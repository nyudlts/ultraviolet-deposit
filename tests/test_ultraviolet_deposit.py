# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 NYU.
#
# Ultraviolet-Deposit is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Module tests."""

from flask import Flask
from ultraviolet_deposit import UltravioletDeposit
import sys


def test_version():
    """Test version import."""
    from ultraviolet_deposit import __version__
    assert __version__


def test_init():
    """Test extension initialization."""
    app = Flask('testapp')
    ext = UltravioletDeposit(app)
    assert 'ultraviolet-deposit' in app.extensions

    app = Flask('testapp')
    ext = UltravioletDeposit()
    assert 'ultraviolet-deposit' not in app.extensions
    ext.init_app(app)
    assert 'ultraviolet-deposit' in app.extensions


def test_view( running_app, base_client):
    """Test view."""
    res = base_client.get("/test")
    assert res.status_code == 200
