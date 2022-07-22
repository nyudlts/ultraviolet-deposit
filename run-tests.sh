#!/usr/bin/env bash
# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 NYU.
#
# Ultraviolet-Deposit is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.


# Usage:
#   pipenv run ./run-tests.sh

#check that pipenv is installed
if ! command -v pipenv &> /dev/null
then
    echo "pipenv could not be found"
    exit 1
fi

#check if pytest and fixtures are installed
if ! command -v pipenv run pytest --version&> /dev/null
then
    echo "pytest is not installed"
    exit 1
fi

#make sure docker is installed 
if ! command docker -v  &> /dev/null 
then
    echo "docker is not istalled. Please install it"
    exit 1
fi


#make sure docker is installed 
if ! command docker-compose -v  &> /dev/null 
then
    echo "docker-compose is not istalled. Please install it"
    exit 1
fi

#make sure pytest.ini is present
if ! test -f pytest.ini
then
    echo "pytest.ini does not exists. Are you in the right directory ?"
    exit 1
fi

#check that requirements are met if we are doing E2E testing
if [ "${E2E}" == 'yes' ]
then
   #check that chromedriver is installed
   if ! command -v chromedriver &> /dev/null
   then
      echo "Chromedriver could not be found. You can not run e2e testing"
      exit 1
   fi
   #check that selenium client is installed
   if ! pipenv graph | grep 'selenium'
   then
      echo "Selenium client is not installed. You can not run e2e testing"
      exit 1
   fi
fi



# Quit on errors
set -o errexit

# Quit on unbound symbols
set -o nounset

# Always bring down docker services
#function cleanup() {
#    eval "$(docker-services-cli down --env)"
#}
#trap cleanup EXIT

#python -m check_manifest --ignore ".*-requirements.txt"
#python -m sphinx.cmd.build -qnNW docs docs/_build/html

docker-compose up -d

python -m pytest
tests_exit_code=$?
#python -m sphinx.cmd.build -qnNW -b doctest docs docs/_build/doctest
exit "$tests_exit_code"
