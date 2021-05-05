#!/bin/bash
source /home/ubuntu/Project/ProjectName/kwp/env/bin/activate
exec gunicorn -c "/home/ubuntu/Project/ProjectName/kwp/gunicorn_config.py" kwp.wsgi