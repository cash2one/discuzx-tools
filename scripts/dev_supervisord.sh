#!/bin/bash

base_path=$(cd `dirname dirname $0`; pwd)
/home/kylin/Program//pyenvs/quant_tools/bin/supervisord -c ${base_path}/deploy/supervisor_dev.conf
