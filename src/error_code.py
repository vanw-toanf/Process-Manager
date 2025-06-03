"""
File: error_code.py
Description: This file defines an enumeration class `CommonErrorCode`
that contains common error codes used in the Process Manager project.

Copyright (C) 2024  Giang Trinh, VuongNQ, and the development team.

This file is part of the Process Manager project and is licensed
under the GNU General Public License v3 or later.
"""

from enum import Enum

class CommonErrorCode(Enum):
    #[ 0 - 20 ] Common Nontify
    OK = 0
    END_SIG = 1
    NOT_END_SIG = 2
    CHECKED = 3
    NOT_CHECKED = 4
    DEBUG = 5
    NOT_DEBUG = 6
    STOP_SIG = 7
    NOT_STOP_SIG = 8


    #[ -20 -> -1 ] special negative signals
    UNKNOWN_ERROR = -1

    #[ -50 -> -21 ] display curses error
    ERROR_INVALID_MIN_SIZE = -21
    ERROR_SIZE_CHANGED = -22


#debug mode
#Change to CommonErrorCode.DEBUG to enable debug
#Change to CommonErrorCode.NOT_DEBUG to disable debug
debug = CommonErrorCode.NOT_DEBUG
