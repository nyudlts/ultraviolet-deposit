..
    Copyright (C) 2021 NYU.

    Ultraviolet-Deposit is free software; you can redistribute it and/or
    modify it under the terms of the MIT License; see LICENSE file for more
    details.

=====================
 Ultraviolet-Deposit
=====================


This repository is a custom deposit module for UltraViolet and it will be used as an extension in the main UltraViolet project.

This module can be added to the main UltraViolet project by running the command below in the local UltraViolet root folder

```
invenio-cli packages install git+https://github.com/nyudlts/ultraviolet-deposit#egg=ultraviolet-deposit
```

If we are doing changes in the module and want to add the new version to the local instance of UltraViolet we can run

```
invenio-cli packages install <path to the local copy of the deposit-module>
```

To run tests separately

Make sure you use node 14 and python 3.8

```
pipenv install --pre --dev
```

```
pipenv run pip install -e .
```

If you want to run E2E

```
export E2E='yes'
```

Before running E2E make sure that Selenium Client is installed and Chrome Webdriver is installed and added to you path.

[Installation instructions](https://www.selenium.dev/selenium/docs/api/py/)


```
pipenv run ./run-tests.sh
```
