# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 NYU.
#
# Ultraviolet-Deposit is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Custom Deposit for Ultraviolet"""

# TODO: This is an example file. Remove it if your package does not use any
# extra configuration variables.

ULTRAVIOLET_DEPOSIT_DEFAULT_VALUE = 'ultraviolet'
"""Default value for the application."""

ULTRAVIOLET_DEPOSIT_BASE_TEMPLATE = 'ultraviolet_deposit/base.html'
"""Default base template for the demo page."""

# Default values for deposit form
ULTRAVIOLET_DEPOSIT_APP_RDM_DEPOSIT_FORM_DEFAULTS = {
    "publisher": "UltraViolet"
}

ULTRAVIOLET_DEPOSIT_CONFIG = {
    "components": {
        "limits": {
            "files_limit": "20",
            "storage_limit": "10Mb",
            "embargo_limit": "1Y"
        }
    }
}
