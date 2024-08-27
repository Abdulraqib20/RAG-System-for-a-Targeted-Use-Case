import asyncio, gc, secrets, uvicorn, re
from src.api_models.chat_model import ChatRequest
from src.agent.llm import LLM_Model
# from src.inference import StreamConversation
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request, Response, status, Depends
from src.config.settings import get_settings
from src.config import appconfig
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
# from src.utilities.Printer import Printer
from fastapi.security import HTTPBasic, HTTPBasicCredentials

# application settings
settings = get_settings()

# description from API documentation
description = f"""
{settings.API_STR} helps you do some awesome stuff. 🚀
"""

# garbage collection to free up resources
gc.collect()

# instantiate basicAuth
TIMEOUT_KEEP_ALIVE = 360

def get_current_username(credentials: HTTPBasicCredentials=Depends(security)):
    """This function sets up the basic with url protection and returns the credential name.

    Args:
        credentials (HTTPBasicCredentials): Basic auth credentials
    
    Raises:
        HTTPException: If the username is invalid.
    Returns:
        str: the username from the credentials.
    """
    
    correct_username = secrets.compare_digest(credentials.username, app_config.auth_user)
    correct_password = secrets.compare_digest(credentials.password, app_config.auth_pass)
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
        
    return credentials.username

api_llm = LLM_Model()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Context manager for application lifespan
    This function initializes and cleans up resources during the application's lifecycle.
    """
    print()




