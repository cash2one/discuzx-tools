#!/bin/bash

base_path=$(cd `dirname $0`; pwd)
/opt/myenvs/quant_tools/bin/supervisord -c ${base_path}/conf/supervisor_app.conf
