#!/bin/bash

docker=$1

if [ "$docker" -eq 0 ]; then
    supervisorctl -c /home/kylin/Luntan/service-quant/deploy/supervisor_run.conf
else
    /home/kylin/Program//pyenvs/quant_tools/bin/supervisorctl -c /home/kylin/Luntan/service-quant/deploy/supervisor_run.conf
fi
