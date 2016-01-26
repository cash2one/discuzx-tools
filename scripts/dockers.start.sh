#!/usr/bin/env bash

docker=$1

if [ "$docker" -eq 0 ]; then
    supervisord -c /home/kylin/Luntan/service-quant/conf/supervisor_run.conf
else
    /home/kylin/MyEnvs/kydiscuzx/bin/supervisord -c /home/kylin/Luntan/service-quant/conf/supervisor_run.conf
fi
