# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 NYU
#
# Ultraviolet-Deposit is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Custom Deposit for Ultraviolet"""

# TODO: This is an example file. Remove it if you do not need it, including
# the templates and static folders as well as the test case.

from flask import Blueprint, render_template
from flask_babelex import gettext as _

blueprint = Blueprint(
    'ultraviolet_deposit',
    __name__,
    template_folder='templates',
    static_folder='static',
)
