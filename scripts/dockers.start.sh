#!/usr/bin/env bash

docker=$1

if [ "$docker" -eq 0 ]; then
    supervisord -c ../deploy/supervisor_run.conf
else
    supervisorctrl -c ../deploy/supervisor_run.conf
fi
