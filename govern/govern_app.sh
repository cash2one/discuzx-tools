#!/usr/bin/env bash

NAME="govern"                                  # Name of the application
DJANGODIR=/opt/websites/service-quant/govern   # Django project directory
SOCKFILE=/opt/work/tmp/gunicorn.sock          # we will communicte using this unix socket

USER=root                                      # the user to run as
GROUP=root                                     # the group to run as
NUM_WORKERS=4                                  # how many worker processes should Gunicorn spawn

DJANGO_SETTINGS_MODULE=govern.settings         # which settings file should Django use
DJANGO_WSGI_MODULE=govern.wsgi                 # WSGI module name

INFO_FILE=/opt/work/log/govern_info.log
ERROR_FILE=/opt/work/log/govern_error.log

PORT=8000
SERVER_NAME=0.0.0.0

echo "Starting $NAME as `whoami`"
# Activate the virtual environment
cd $DJANGODIR

source /opt/myenvs/kydjango/bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)

test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec /opt/myenvs/kydjango/bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user=$USER --group=$GROUP \
  --log-level=debug \
  --bind=$SERVER_NAME:$PORT \
  --log-file FILE=$INFO_FILE \
  --error-logfile=$ERROR_FILE
