"""Initialize Config class to access environment variables."""
from dotenv import load_dotenv
import os

load_dotenv()

class Config(object):
    """Set environment variables."""

    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    # This is the secret key for WTF forms ##
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-me')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True
    # Optional: disable CSRF token expiry in dev to reduce 403s from stale pages
    WTF_CSRF_TIME_LIMIT = None
