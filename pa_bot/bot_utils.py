# -*- coding: utf-8 -*-
"""
Bot utilities.

This module exposes utilities for miscellaneous tasks related to Discord. 
"""


def say(bot,
        message,
        code_formatting: bool = True,
        syntax_highlight: str = ""):

    if code_formatting:
        to_send = "```{0}\n{1}\n```".format(syntax_highlight, message)
    else:
        to_send = message
    return bot.say(to_send)
