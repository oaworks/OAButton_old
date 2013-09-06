
import os

PGSQL_HOST = os.environ['PGSQL_HOST']
PGSQL_DB = os.environ['PGSQL_DB']
PGSQL_USER = os.environ['PGSQL_USER']
PGSQL_PASS = os.environ['PGSQL_PASS']

DEFAULT_DB = {
    'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
    'NAME': PGSQL_DB,
    'USER': PGSQL_USER,
    'PASSWORD': PGSQL_PASS,
    'HOST': PGSQL_HOST,
    'PORT': 5432,
}

MONGO_URI = os.environ['MONGOLAB_URI']
MONGO_DBNAME = os.environ['MONGO_DBNAME']
