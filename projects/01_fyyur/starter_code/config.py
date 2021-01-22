import os

SECRET_KEY = os.urandom(32)

basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
SQLALCHEMY_DATABASE_URI = 'postgres://michalozieblo@localhost:5432/udacityFyyur'
SQLALCHEMY_TRACK_MODIFICATIONS = False
