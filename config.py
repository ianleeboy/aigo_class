import os

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://ianlee:B8d8LHNIQWdy1oaLyxX3Y3TmjVmw90Zq@dpg-cjbik3c5kgrc73a7i060-a.singapore-postgres.render.com/line_cp92'

class ProdConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')