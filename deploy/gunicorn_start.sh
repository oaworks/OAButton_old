#!/bin/bash

NAME="OAButton"                                  # Name of the application
DJANGODIR=/home/ubuntu/dev/OAButton           # Django project directory
USER=ubuntu                           # the user to run as
GROUP=ubuntu                       # the group to run as
NUM_WORKERS=10                                     # how many worker processes should Gunicorn spawn
DJANGO_SETTINGS_MODULE=oabutton.settings         # which settings file should Django use
DJANGO_WSGI_MODULE=oabutton.wsgi           # WSGI module name

echo "Starting $NAME"

# Activate the virtual environment
cd $DJANGODIR
source /home/ubuntu/.virtualenvs/oabutton/bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH


# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec /home/ubuntu/.virtualenvs/oabutton/bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
  --preload \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user=$USER --group=$GROUP \
  --log-level=debug \
  --bind=localhost:8000
