..
    Copyright (C) 2021 NYU.

    Ultraviolet-Deposit is free software; you can redistribute it and/or
    modify it under the terms of the MIT License; see LICENSE file for more
    details.

=====================
 Ultraviolet-Deposit
=====================


Custom Deposit for Ultraviolet

Will be used as an extention in main Ultraviolet project.

Could be added to the main Ultraviolet project by running the command below in ultraviolet root folder

```
invenio-cli packages install git+https://github.com/nyudlts/ultraviolet-deposit#egg=ultraviolet-deposit
```

If we are doing changes in the module and want to add the new version to the local instance of ultraviole we can run 

```
invenio-cli packages install <path to the local copy of the demposit-module>
```

To run tests separately

Make sure you use node 14 and python 3.8

```
pipenv install --pre
```

```
pipenv run invenio webpack buildall
```

If you want to run E2E 

```
export E2E='yes'
```

```
./run-tests.sh
```
