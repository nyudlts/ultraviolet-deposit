# -*- coding: utf-8 -*-
#
# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 NYU.
#
# ultraviolet is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
"""E2E test of the front page."""

from flask import url_for
from selenium.webdriver.common.by import By
import multiprocessing
import logging
import sys

"""This is needed so live_server fixture can be used on Mac with python3.8 
    https://github.com/pytest-dev/pytest-flask/issues/104 """
multiprocessing.set_start_method("fork")


def test_frontpage(running_app, live_server, browser):
    """Test retrieval of front page."""
    browser.get(url_for('test_deposit.deposit_form', _external=True))
    print( browser.get_log('browser'), file=sys.stderr)
    assert "UltraViolet" == browser.find_element(By.TAG_NAME, "h1").text