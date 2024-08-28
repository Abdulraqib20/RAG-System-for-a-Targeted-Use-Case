from llama_index.core.memory import ChatMemoryBuffer
import os
from dotenv import load_dotenv; load_dotenv()
import time
import traceback
from cachetools import TTLCache
# from functools import lru_cache
# import json


# Set up cache
CACHE_MAXSIZE = 100  # Maximum number of items in cache
CACHE_TTL = 3600  # Time to live for cache items (in seconds)
conversation_cache = TTLCache(maxsize=CACHE_MAXSIZE, ttl=CACHE_TTL)

MEMORY_TOKEN_LIMIT = 1500  # Example value, adjust as needed

def print_log(message, level='info'):
    """Logs a message with a specified log level."""
    levels = {
        'info': '\033[94m',   # Blue
        'warning': '\033[93m', # Yellow
        'error': '\033[91m',   # Red
        'reset': '\033[0m'     # Reset color
    }
    color = levels.get(level, levels['info'])
    print(f"{color}{level.upper()}: {message}{levels['reset']}")




def get_conversation_history(conn, conversation_uuid):
    if conversation_uuid is None or conversation_uuid == '':
        return ChatMemoryBuffer(token_limit=MEMORY_TOKEN_LIMIT)

    start_time = time.time()

    # Check if conversation history is in cache
    cached_history = conversation_cache.get(conversation_uuid)
    if cached_history:
        print_log(f"Retrieved conversation history from cache in {time.time() - start_time} seconds.")
        return ChatMemoryBuffer.from_dict(cached_history)

    memory_instance = ChatMemoryBuffer(token_limit=MEMORY_TOKEN_LIMIT)
    history = []

    print_log("Retrieving conversation history from database...")
    print_log(f"Conversation UUID: {conversation_uuid}")

    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT sender, message FROM messages 
                WHERE conversation_uuid = %s 
                ORDER BY created_at ASC
            """, (conversation_uuid,))
            messages = cur.fetchall()

        for message in messages:
            sender, content = message
            history.append({
                'additional_kwargs': {},
                'content': content,
                'role': 'assistant' if sender == 'assistant' else 'user'
            })

        # memory_dict = {'chat_history': list(reversed(history)), 'token_limit': MEMORY_TOKEN_LIMIT}
        memory_dict = {'chat_history': list(reversed(history)), 'token_limit': MEMORY_TOKEN_LIMIT}
        conversation_cache[conversation_uuid] = memory_dict


        try:
            memory = memory_instance.from_dict(memory_dict)
            # Cache the conversation history
            conversation_cache[conversation_uuid] = memory_dict
        except Exception as e:
            exception_trace = traceback.format_exc()
            print_log(f"Error loading conversation history: {exception_trace}", 'error')
            return ChatMemoryBuffer(token_limit=MEMORY_TOKEN_LIMIT)

        print_log(f"Conversation history loaded and cached in {time.time() - start_time} seconds.")
        return memory

    except psycopg2.Error as e:
        print_log(f"Database error: {e}", 'error')
        return None
    
    
def update_conversation_cache(conversation_uuid, sender, message):
    cached_history = conversation_cache.get(conversation_uuid)
    if cached_history is None:
        cached_history = {'chat_history': [], 'token_limit': MEMORY_TOKEN_LIMIT}
    elif 'chat_history' not in cached_history:
        cached_history['chat_history'] = []
    
    new_message = {
        'additional_kwargs': {},
        'content': message,
        'role': 'assistant' if sender == 'assistant' else 'user'
    }
    cached_history['chat_history'].insert(0, new_message)
    conversation_cache[conversation_uuid] = cached_history
    print_log(f"Cache updated for conversation {conversation_uuid}")
    

def insert_message(conn, conversation_uuid, sender, message):
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO messages (conversation_uuid, sender, message)
                VALUES (%s, %s, %s)
            """, (conversation_uuid, sender, message))
        conn.commit()
        update_conversation_cache(conversation_uuid, sender, message)
        print_log(f"Message inserted and cache updated for conversation {conversation_uuid}")
    except psycopg2.Error as e:
        print_log(f"Error inserting message: {e}", 'error')
        conn.rollback()
        

def clear_conversation_cache(conversation_uuid=None):
    if conversation_uuid:
        conversation_cache.pop(conversation_uuid, None)
        print_log(f"Cache cleared for conversation {conversation_uuid}")
    else:
        conversation_cache.clear()
        print_log("All conversation caches cleared")