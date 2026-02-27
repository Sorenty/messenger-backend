import os
from dotenv import load_dotenv

load_dotenv()  # загружает .env в dev, безопасно — в проде использовать реальные env

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///dev.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False