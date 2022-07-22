#! /usr/bin/env bash

# REQUIRES: curl, git

curl -L https://raw.githubusercontent.com/pyenv/pyenv-installer/master/bin/pyenv-installer | bash

echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n eval "$(pyenv init --path)"\nfi' >> ~/.bashrc

curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash

source ~/.bashrc

pyenv install 3.8.12
pyenv local 3.8.12
nvm install 14.17.3
nvm use 14

# Install docker-compose, cookiecutter and pipenv for the user
pip install --user cookiecutter pipenv docker-compose


cd ultraviolet-deposit

set -e


script_path=$(dirname "$0")
pipfile_lock_path="$script_path/../Pipfile.lock"

if [ ! -f "$pipfile_lock_path" ]; then
    echo "'Pipfile.lock' not found. Generating via 'pipenv lock --dev'..."
    pipenv lock --dev --pre
fi

# Installs all packages specified in Pipfile.lock
pipenv sync --dev --pre
# Install application code and entrypoints from 'setup.py'
pipenv run pip install -e .
# Build assets
nvm use 14
pipenv run invenio collect 
pipenv run invenio webpack buildall

wget "https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm"
sudo yum -y localinstall google-chrome-stable_current_x86_64.rpm

echo 'export PATH=$PATH:/home/vagrant/bin' >> ~/.bashrc
