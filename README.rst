..
    Copyright (C) 2021 NYU.

    Ultraviolet-Deposit is free software; you can redistribute it and/or
    modify it under the terms of the MIT License; see LICENSE file for more
    details.

=====================
 Ultraviolet-Deposit
=====================


This repository is a custom deposit module for UltraViolet, and it will be used as an extension in the main UltraViolet project.

This module can be added to the main UltraViolet project by running the command below in the local UltraViolet root folder

```
invenio-cli packages install git+https://github.com/nyudlts/ultraviolet-deposit#egg=ultraviolet-deposit
```

If we are doing changes in the module and want to add the new version to the local instance of UltraViolet we can run

```
invenio-cli packages install <path to the local copy of the deposit-module>
```

Any development with the module will require testing. To run tests separately, make sure you are using node 14, nvm 6 and python 3.8. Also, the ElasticSearch container must be running (check by running `docker ps`)

The testing process is:

```
pipenv install --pre --dev
```

```
pipenv run pip install -e .
```

```
pipenv run invenio webpack clean
```

```
pipenv run invenio webpack buildall
```

If you want to run E2E tests use

```
export E2E='yes'
```

Before running E2E make sure that Selenium Client is installed and Chrome Webdriver is installed and added to your path.

- [Selenium installation instructions](https://www.selenium.dev/selenium/docs/api/py/)
- [Chrome Webdriver installation instructions](https://formulae.brew.sh/cask/chromedriver) - Note that if you install via HomeBrew on a Mac, you will have to go to your security permissions and allow ChromeDriver before running the E2E test.


```
pipenv run ./run-tests.sh
```
