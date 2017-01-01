#!/bin/bash

base_path=$(cd `dirname $0`; pwd)
/home/kylin/Program/myenvs/quant_tools/bin/supervisord -c ${base_path}/conf/supervisor_dev.conf
