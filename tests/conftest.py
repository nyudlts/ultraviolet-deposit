# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 NYU.
#
# Ultraviolet-Deposit is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Pytest configuration.

See https://pytest-invenio.readthedocs.io/ for documentation on which test
fixtures are available.
"""

import shutil
import sys

import pytest
from flask import Flask, render_template
from flask_babelex import Babel

from ultraviolet_deposit.ext import UltravioletDeposit
from ultraviolet_deposit.views import blueprint



@pytest.fixture(scope='module')
def celery_config():
    """Override pytest-invenio fixture.

    TODO: Remove this fixture if you add Celery support.
    """
    return {}


@pytest.fixture(scope='module')
def create_app(instance_path):
    """Application factory fixture."""
    def factory(**config):
        app = Flask('testapp', instance_path=instance_path)
        app.config.update(**config)
        Babel(app)
        UltravioletDeposit(app)
        app.register_blueprint(blueprint)
        app.template_folder = 'tests'
        @app.route("/")
        def deposit_form():
            """Deposit form fixture."""
            return render_template(
                "index.html",
            )
        return app
    return factory
