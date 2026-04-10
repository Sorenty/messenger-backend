import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///dev.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SESSION_TYPE = os.getenv("SESSION_TYPE", "filesystem")
    SESSION_REDIS_URL = os.getenv("SESSION_REDIS_URL", "redis://localhost:6379/1")
    SESSION_PERMANENT = False

    SERVICE_NAME = os.getenv("SERVICE_NAME", "messenger-backend")
    APP_VERSION = os.getenv("APP_VERSION", "dev")
    WEB_CONCURRENCY = int(os.getenv("WEB_CONCURRENCY", "2"))