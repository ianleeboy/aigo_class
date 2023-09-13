import os

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    LINE_PAY_ID = '2000604809'
    LINE_PAY_SECRET = 'c68fdc6cccb2076b07aed3920777a3e6'

    STORE_IMAGE_URL = 'https://i.imgur.com/c0HMasX.jpg'

class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://ianlee:IsN7ToAuqAxNaN0Mq2COqK844DI7WaSb@dpg-cjg2n3b6fquc73ald0r0-a.singapore-postgres.render.com/robot'

class ProdConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')