#!/bin/bash

base_path=$(cd `dirname $0`; pwd)
/opt/myenvs/quant_tools/bin/supervisorctl -c ${base_path}/conf/supervisor_app.conf
