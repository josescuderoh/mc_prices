#!/bin/bash

NAME="prices_api"                                   # Name of the application
DJANGODIR=/usr/local/apps/prices_api/src/prices_api               # Django project
SOCKFILE=/usr/local/virtualenvs/prices_api/run/gunicorn.sock  # we will communicte using this unix socket
USER=root                                         # the user to run as
NUM_WORKERS=3                                       # how many worker processes should Gunicorn spawn
DJANGO_SETTINGS_MODULE=prices_api.settings      # which settings file should Django use
DJANGO_WSGI_MODULE=prices_api.wsgi              # WSGI module name
echo "Starting $NAME as `whoami`"

# Make sure the virtual environment is activated

cd $DJANGODIR
source /usr/local/virtualenvs/prices_api/bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH
source /home/ubuntu/credentials/cred.bash

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || sudo mkdir -p $RUNDIR

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)

exec gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user=$USER --group=$GROUP \
  --bind=unix:$SOCKFILE \
  --log-level=debug \
  --log-file= /var/log/gunicorn_prices_api.log
