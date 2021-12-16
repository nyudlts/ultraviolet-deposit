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
from time import sleep
import pytest
import config


"""This is needed so live_server fixture can be used on Mac with python3.8 
    https://github.com/pytest-dev/pytest-flask/issues/104 """
multiprocessing.set_start_method("fork")

def test_upload_form(running_app, live_server, browser):
    """Test retrieval of upload page."""
    browser.get(url_for('test_deposit.deposit_form', _external=True))
    print(browser.get_log('browser'), file=sys.stderr)
    assert "New upload" == browser.find_element(By.TAG_NAME, "h1").text

@pytest.mark.parametrize("select_field, search_key, assert_value",[("languages","Eng","English"),("resource_type","Data","Dataset")])
def test_remote_select(running_app, live_server, browser,select_field, search_key, assert_value):
    """Test retrieval of upload page."""
    browser.get(url_for('test_deposit.deposit_form', _external=True))
    dropdown = browser.find_element(By.NAME, "metadata."+select_field)

    input_search = dropdown.find_element(By.TAG_NAME, "input")
    input_search.click()
    input_search.clear()
    input_search.send_keys(search_key)
    sleep(90)

    dropdown_values = dropdown.find_element(By.CLASS_NAME, "visible.menu.transition")
    assert assert_value == dropdown_values.find_element(By.CLASS_NAME, "selected.item").text

def test_configs_passed(running_app, live_server, browser):
    """Test retrieval of upload page."""
    browser.get(url_for('test_deposit.deposit_form', _external=True))
    deposits_limits = browser.find_element(By.NAME, "deposits-limits")

    assert deposits_limits is not None
