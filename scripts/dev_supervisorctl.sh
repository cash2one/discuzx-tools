#!/bin/bash

base_path=$(cd `dirname $0`; pwd)
/home/kylin/Program/myenvs/quant_tools/bin/supervisorctl -c ${base_path}/conf/supervisor_dev.conf
