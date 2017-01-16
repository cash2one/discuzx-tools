#!/bin/bash

docker=$1

if [ "$docker" -eq 0 ]; then
    supervisord -c ../deploy/supervisor_run.conf
else
    supervisorctl -c ../deploy/supervisor_run.conf
fi
