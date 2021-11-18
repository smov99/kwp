#!/bin/bash
base_python_interpreter=""
project_domain=""
project_path=`pwd`
debug=""

read -p "Python interpreter (path or name, for example python3.9): " base_python_interpreter
read -p "Your domain without protocol (for example, google.com or _ to use ip address): " project_domain
read -p "Debug flag (True or False): " debug
`$base_python_interpreter -m venv env`
source env/bin/activate
pip install -U pip
pip install -r requirements.txt

sed -i "s~dbms_template_path~$project_path~g" nginx/site.conf systemd/gunicorn.service systemd/celery.service
sed -i "s~dbms_template_domain~$project_domain~g" nginx/site.conf
sed -i "s~dbms_template_debug~$debug~g" kwp/ansible_settings.py

sudo ln -s $project_path/nginx/site.conf /etc/nginx/sites-enabled/
sudo ln -s $project_path/systemd/gunicorn.service /etc/systemd/system/
sudo ln -s $project_path/systemd/celery.service /etc/systemd/system/

sudo systemctl daemon-reload
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
sudo systemctl start celery
sudo systemctl enable celery
sudo service nginx restart