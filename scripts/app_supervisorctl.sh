#!/bin/bash

base_path=$(cd `dirname $0`; pwd)
/opt/Program/pyenvs/quant_tools/bin/supervisorctl -c ${base_path}/deploy/supervisor_app.conf
