command = '/home/ubuntu/Project/ProjectName/kwp/env/bin/gunicorn'
pythonpath = '/home/ubuntu/Project/ProjectName/kwp'
bind = '127.0.0.1:8001'
workers = 5
user = 'ubuntu'
limit_request_fields = 32000
limit_request_fields_size = 0
raw_env = 'DJANGO_SETTINGS_MODULE=kwp.settings'
