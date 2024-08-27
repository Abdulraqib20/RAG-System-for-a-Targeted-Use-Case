from pydantic import BaseModel

class UserData(BaseModel):
    sentence: str

class ChatRequest():
    """Request model for chat requests.
    the message from the user.
    """
    
    sentence: str
    UserId: str

# {
#     "sentence":""
# }
    
