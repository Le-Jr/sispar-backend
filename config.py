from os import environ
from dotenv import load_dotenv

load_dotenv()

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = environ.get("URL_DATABASE_DEV")  

class ProductionConfig(Config):
    DEBUG = False
    # URL do PostgreSQL fornecida pelo Render
    SQLALCHEMY_DATABASE_URI = environ.get("DATABASE_URL")
    
    @classmethod
    def init_app(cls, app):
        if cls.SQLALCHEMY_DATABASE_URI and cls.SQLALCHEMY_DATABASE_URI.startswith('postgres://'):
            cls.SQLALCHEMY_DATABASE_URI = cls.SQLALCHEMY_DATABASE_URI.replace('postgres://', 'postgresql://', 1)

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}