from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Database credentials
DATABASE_HOSTNAME = "localhost"
DATABASE_USERNAME = "postgres"
DATABASE_NAME = "shared_models"
DATABASE_PASSWORD = "Mahesh%40204"
DATABASE_PORT = "5432"

DATABASE_URL = f"postgresql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOSTNAME}:{DATABASE_PORT}/{DATABASE_NAME}"

# SQLAlchemy setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base for all models
Base = declarative_base()
