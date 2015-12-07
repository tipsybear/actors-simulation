# gvas.console.utils
# Console utility functions and helpers
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Tue Nov 24 17:35:49 2015 -0500
#
# Copyright (C) 2015 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: utils.py [] benjamin@bengfort.com> $

"""
Console utility functions and helpers
"""

##########################################################################
## Imports
##########################################################################

import colorama

##########################################################################
## Console colors
##########################################################################

def color_format(string, color, *args, **kwargs):
    """
    Implements string formating along with color specified in colorama.Fore
    """
    string = string.format(*args, **kwargs)
    return color + string + colorama.Fore.RESET
