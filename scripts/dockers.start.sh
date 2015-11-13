#!/usr/bin/env bash

sudo service redis-server start
/home/kylin/MyEnvs/kydiscuzx/bin/supervisord -c /home/kylin/Luntan/service-quant/conf/supervisor_run.conf
