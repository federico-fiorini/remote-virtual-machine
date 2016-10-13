# Update apt-get and install required packages
apt-get update
apt-get install git build-essential python python-dev python-pip libffi-dev libssl-dev

# Install virtualenv
pip install --upgrade pip virtualenv

# Create virtual environments
virtualenv front-end/.env
front-end/.env/bin/pip install -r front-end/requirements.txt

virtualenv back-end/.env
back-end/.env/bin/pip install -r back-end/requirements.txt

