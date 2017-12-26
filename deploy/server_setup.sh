#!/usr/bin/env bash

# TODO: Set to URL of git repo.
PROJECT_GIT_URL='https://github.com/josescuderoh/mc_prices.git'
PROJECT_BASE_PATH='/usr/local/apps'
VIRTUALENV_BASE_PATH='/usr/local/virtualenvs'

# Set Ubuntu Language
sudo locale-gen en_GB.UTF-8

# Install Python,supervisor, nginx and pip
sudo apt-get update
sudo apt-get install -y python3-dev python-pip supervisor nginx git

# Upgrade pip to the latest version.
sudo pip install --upgrade pip
sudo pip install virtualenv

sudo mkdir -p $PROJECT_BASE_PATH
sudo git clone $PROJECT_GIT_URL $PROJECT_BASE_PATH/prices_api

sudo mkdir -p $VIRTUALENV_BASE_PATH
sudo virtualenv -p python3 $VIRTUALENV_BASE_PATH/prices_api
sudo chown -R ubuntu:ubuntu /usr/local/virtualenvs/prices_api

source $VIRTUALENV_BASE_PATH/prices_api/bin/activate
pip install -r $PROJECT_BASE_PATH/prices_api/requirements.txt

#Create executables for supervisor
cd $PROJECT_BASE_PATH/prices_api/deploy
sudo chmod +x gunicorn_start.bash

#Create log files
sudo mkdir /var/log/prices_api
sudo touch /var/log/prices_api/nginx-access.log
sudo touch /var/log/prices_api/nginx-error.log
sudo touch /var/log/prices_api/prices_api.log
sudo touch /var/log/prices_api/prices_api_err.log

# Setup Supervisor to run our uwsgi process.
sudo cp $PROJECT_BASE_PATH/prices_api/deploy/supervisor_prices_api.conf /etc/supervisor/conf.d/prices_api.conf
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl restart prices_api

# Setup nginx to make our application accessible.
sudo cp $PROJECT_BASE_PATH/prices_api/deploy/nginx_prices_api.conf /etc/nginx/sites-available/prices_api.conf
sudo ln -s /etc/nginx/sites-available/prices_api.conf /etc/nginx/sites-enabled/prices_api.conf
sudo systemctl restart nginx.service

echo "DONE! :)"
