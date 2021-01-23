import os

DB_HOST = os.environ.get('DB_HOST')
DB_USR = os.environ.get('DB_USR')
DB_PASSWD = os.environ.get('DB_PASSWD')

if not all([DB_HOST, DB_USR, DB_PASSWD]):
   raise Exception('Missing database environment variables!')

DB_URL = 'postgres://{}:{}@{}/udacityFyyur'

SECRET_KEY = os.urandom(32)

basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

SQLALCHEMY_TRACK_MODIFICATIONS = False
