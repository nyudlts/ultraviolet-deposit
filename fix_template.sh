#!/bin/bash

path_template=$(pipenv --venv)
echo $path_template
mkdir $path_template"/var/instance/templates"
