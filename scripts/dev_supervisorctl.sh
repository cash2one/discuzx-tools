#!/bin/bash

base_path=$(cd `dirname $0`; pwd)
/home/kylin/Program//pyenvs/quant_tools/bin/supervisorctl -c ${base_path}/deploy/supervisor_dev.conf
