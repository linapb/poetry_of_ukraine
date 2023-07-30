import os
from dotenv import load_dotenv
load_dotenv()  # Exports variables to environment from .env file in current folder


class Config:
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

    SESSION_PERMANENT = False
    SESSION_TYPE = "filesystem"

    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    DEBUG = True


# Just example
class TestingConfig(Config):
    DATABASE_URI = 'sqlite:///:memory:'
    TESTING = True


class ProductionConfig(Config):
    pass