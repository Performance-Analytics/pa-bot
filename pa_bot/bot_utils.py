# -*- coding: utf-8 -*-
"""
Bot utilities.

This module exposes utilities for miscellaneous tasks related to Discord. 
"""


from types import BuiltinFunctionType
from typing import List


def pendular_apply(target, *args):
    if isinstance(target, BuiltinFunctionType):
        parity = 0
        while parity <= len(args):
            try:
                return target(*args[:parity])
            except TypeError:
                parity += 1
        raise TypeError("too few arguments supplied; expected >= {0} but got {1}"
                        .format(parity, len(args)))
    else:
        return target


def say(bot,
        message,
        code_formatting: bool = True,
        syntax_highlight: str = ""):

    if code_formatting:
        to_send = "```{0}\n{1}\n```".format(syntax_highlight, message)
    else:
        to_send = message
    return bot.say(to_send)
