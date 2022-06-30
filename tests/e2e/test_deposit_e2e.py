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
from selenium.webdriver.common.alert import Alert
import multiprocessing
import logging
import sys
from time import sleep
import pytest


"""This is needed so live_server fixture can be used on Mac with python3.8 
    https://github.com/pytest-dev/pytest-flask/issues/104 """
multiprocessing.set_start_method("fork")

def test_upload_form(running_app, live_server, browser):
    """Test retrieval of upload page."""
    browser.get(url_for('test_deposit.deposit_form', _external=True))
    print(browser.get_log('browser'), file=sys.stderr)
    assert "New upload" == browser.find_element(By.TAG_NAME, "h1").text

@pytest.mark.parametrize("select_field, search_key, assert_value",[
    ("languages","Eng","English"),
    ("resource_type","Data","Dataset")])
def test_languages(running_app, live_server, browser, select_field, search_key, assert_value):
    """Test Languages Dropdown"""
    browser.get(url_for('test_deposit.deposit_form', _external=True))
    dropdown = browser.find_element(By.NAME, "metadata."+select_field)

    input_search = dropdown.find_element(By.TAG_NAME, "input")
    input_search.click()
    input_search.clear()
    input_search.send_keys(search_key)
    sleep(30)

    dropdown_values = dropdown.find_element(By.CLASS_NAME, "visible.menu.transition")
    assert assert_value == dropdown_values.find_element(By.CLASS_NAME, "selected.item").text


@pytest.mark.parametrize("select_field, search_key, assert_value",[
    ("related_work", "Machine", "Machine Learning"),
    ("alternate_identifier", "Alternate", "Alternate Identifier 1")])
def test_dropdowns(running_app, live_server, browser, select_field, search_key, assert_value):
    """Test Related Work and Alternate Identifiers Dropdowns"""
    browser.get(url_for('test_deposit.deposit_form', _external=True))
    print(browser.get_log('browser'))
    dropdown = browser.find_element(By.NAME, "metadata."+select_field)

    input_search = dropdown.find_element(By.TAG_NAME, "input")
    input_search.click()
    input_search.clear()
    input_search.send_keys(search_key)
    sleep(30)

    dropdown_values = dropdown.find_element(By.CLASS_NAME, "visible.menu.transition")
    assert assert_value == dropdown_values.find_element(By.CLASS_NAME, "selected.item").text


@pytest.mark.parametrize("input_date, alert_value, publish", [
    ("2022-10-01", "", True),
    ("2023-10-01", "Embargo Date cannot be greater than 1 year from now.", False)])
def test_embargo(running_app, live_server, browser, input_date, alert_value, publish):
    errors = []
    browser.get(url_for('test_deposit.deposit_form', _external=True))

    # Enable Embargo
    embargo_checkbox = browser.find_element(By.ID, "access.embargo.active")
    print("Checkbox Type: {}".format(embargo_checkbox.get_attribute("type")))
    embargo_checkbox.click()
    print(f"Is Active Selected {embargo_checkbox.is_selected()}")

    # Apply Embargo Until Date
    embargo_field = browser.find_element(By.ID, "access.embargo.until")
    embargo_field.send_keys(input_date)

    # Press "Save Draft" Button
    browser.find_element(By.NAME, "save").click()

    if input_date == "2023-10-01":
        publish_state = browser.find_element(By.NAME, "publish").is_enabled()
        if publish != publish_state:
            errors.append("Publish button test fail.")

    print(errors)
    a = Alert(browser)
    if alert_value != a.text:
        errors.append("Embargo Alert Test Fail.")
    a.accept()

    assert not errors, "Errors Occured: \n{}".format("\n".join(errors))

    # assert False == browser.find_element(By.NAME, "publish").is_enabled()
    # assert "Embargo Date cannot be greater than 1 year from now." == browser.switch_to.alert.text