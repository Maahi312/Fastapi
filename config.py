from datetime import timezone
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

class Settings(BaseSettings):
    database_hostname: str
    database_username: str
    database_password: str
    database_name: str
    database_port: str

    class Config:
        env_file = ".env"

settings = Settings()


