from config import appconfig
from pydantic import BaseSettings

class Settings(BaseSettings):
    """
    This class generates the BaseSettings from FASTAPI.
    It contains project definitions, environment configuration,
    and other application settings.

    Args:
        None.
    
    Returns:
        class: extends the BaseSettings class.
    """
    
    # API Configuration
    if appconfig.Env == 'development':
        API_STR: str = '/dev/api/v2'
    else:
        API_STR: str = '/api/v1'
    
    VERSION: str = '3.0.2'
    PROJECT_NAME: str = 'AI Server'
    ENV: str = appconfig.Env

    # Authentication
    # AUTH_USER: str = appconfig.auth_user
    # AUTH_PASS: str = appconfig.auth_pass

    # # Database Configuration
    # MONGO_HOST: str = appconfig.mongo_host
    # MONGO_PORT: str = appconfig.mongo_port
    # MONGO_USER: str = appconfig.mongo_user
    # MONGO_PASSWORD: str = appconfig.mongo_password

    # API Keys
    GROQ_API_KEY: str = appconfig.groq_key
    PINECONE_API_KEY: str = appconfig.pinecone_key
    LANGCHAIN_API_KEY: str = appconfig.langchain_key
    QDRANT_API_KEY: str = appconfig.qdrant_key

    # Application Port
    APP_PORT: int = int(appconfig.app_port) if appconfig.app_port else 8000
    
    class Config:
        """Pydantic model configuration."""
        env_file = ".env"
        case_sensitive = True


def get_settings() -> Settings:
    """
    Returns the Settings object.

    Args:
        None.

    Returns:
        Settings: The settings object containing application configurations.
    """
    return Settings()
