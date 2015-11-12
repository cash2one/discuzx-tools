#!/usr/bin/env bash

sudo redis-server
/home/kylin/MyEnvs/kydiscuzx/bin/supervisord -c /home/kylin/Luntan/service-quant/conf/supervisor_run.conf
tail ../logs/docker_data.log -f
