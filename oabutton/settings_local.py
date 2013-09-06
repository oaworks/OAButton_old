
import os

DEFAULT_DB = {
         'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
         'NAME': 'oabutton.sqlite3',                      # Or path to database file if using sqlite3.
         'USER': '',                      # Not used with sqlite3.
         'PASSWORD': '',                  # Not used with sqlite3.
         'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
         'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
}


# MongoDB settings
MONGO_URI = 'mongodb://localhost:27017/'
MONGO_DBNAME = 'oabutton-server-dev'
