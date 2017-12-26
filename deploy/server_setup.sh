#!/usr/bin/env bash

# TODO: Set to URL of git repo.
PROJECT_GIT_URL='https://github.com/josescuderoh/mc_prices.git'
PROJECT_BASE_PATH='/usr/local/apps'
VIRTUALENV_BASE_PATH='/usr/local/virtualenvs'

# Set Ubuntu Language
locale-gen en_GB.UTF-8

# Install Python, SQLite and pip
apt-get update
sudo apt-get upgrade
apt-get install -y python3-dev python-pip supervisor nginx git postgresql postgresql-contrib

# Upgrade pip to the latest version.
pip install --upgrade pip
pip install virtualenv

mkdir -p $PROJECT_BASE_PATH
git clone $PROJECT_GIT_URL $PROJECT_BASE_PATH/prices_api

mkdir -p $VIRTUALENV_BASE_PATH
virtualenv -p python3 $VIRTUALENV_BASE_PATH/prices_api

source $VIRTUALENV_BASE_PATH/prices_api/bin/activate
pip install -r $PROJECT_BASE_PATH/prices_api/requirements.txt

# Setup Supervisor to run our uwsgi process.
cp $PROJECT_BASE_PATH/prices_api/deploy/supervisor_prices_api.conf /etc/supervisor/conf.d/prices_api.conf
supervisorctl reread
supervisorctl update
supervisorctl restart prices_api

# Setup nginx to make our application accessible.
cp $PROJECT_BASE_PATH/prices_api/deploy/nginx_prices_api.conf /etc/nginx/sites-available/prices_api.conf
ln -s /etc/nginx/sites-available/prices_api.conf /etc/nginx/sites-enabled/prices_api.conf
systemctl restart nginx.service

echo "DONE! :)"
