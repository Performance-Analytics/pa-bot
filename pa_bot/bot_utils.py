# -*- coding: utf-8 -*-
"""
Bot utilities.

This module exposes utilities for miscellaneous tasks related to Discord. 
"""


from typing import List


def render_table(table_list: List[List]) -> str:

    return "\n".join([" | ".join(column) for column in table_list])


def say(bot,
        message,
        code_formatting: bool = True,
        syntax_highlight: str = ""):

    if code_formatting:
        to_send = "```{0}\n{1}\n```".format(syntax_highlight, message)
    else:
        to_send = message
    return bot.say(to_send)
