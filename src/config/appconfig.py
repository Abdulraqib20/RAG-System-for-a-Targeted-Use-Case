from dotenv import load_dotenv;load_dotenv()
import os

Env = os.getenv("PYTHON_ENV")
groq_key = os.getenv("GROQ_API_KEY")
pinecone_key = os.getenv("PINECONE_API_KEY")
langchain_key = os.getenv("LANGCHAIN_API_KEY")
qdrant_key = os.getenv("QDRANT_API_KEY")

vertex_ai_key = os.getenv("VERTEX_AI_KEY")
anthropic_key = os.getenv("ANTHROPIC_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")


# app_port = os.getenv("PORT")
# auth_user = os.getenv("AUTH_USERNAME")
# auth_pass = os.getenv("AUTH_PASSWORD")
# mongo_host = os.getenv("DB_HOST")
# mongo_port = os.getenv("DB_PORT")
# mongo_user = os.getenv("DB_USER")
# mongo_password = os.getenv("DB_PASSWORD")

