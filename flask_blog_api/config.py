import os


class Config:
    TESTING = False
    DEBUG = False
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):

    SECRET_KEY = "dev"
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///flask_blog.sqlite"
    JWT_SECRET_KEY = "super-secret"


class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    SECRET_KEY = "test"
    SQLALCHEMY_DATABASE_URI = "sqlite:///"
    JWT_SECRET_KEY = "test"
