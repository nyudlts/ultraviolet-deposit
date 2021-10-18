# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 NYU.
#
# Ultraviolet-Deposit is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Custom Deposit for Ultraviolet"""

from .ext import UltravioletDeposit
from .version import __version__

__all__ = ('__version__', 'UltravioletDeposit')
