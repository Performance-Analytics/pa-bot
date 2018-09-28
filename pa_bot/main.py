#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Entry point to bot.
"""


from typing import Optional
import logging

from discord.ext import commands

import commands as bot_commands


# Add bot key here.
bot_key: Optional[str] = "NDg4NDI0MDI2NTkxNTkyNDYx.Do_1SA.yrcfJ26WrX9PjgwTczsyKA6gMwI"

# Debug logging mode?
debug: bool = False

if debug:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

bot = commands.Bot(command_prefix=",", description="Performance Analytics bot")


@bot.event
async def on_ready():

    print('Logged in as')
    print(bot.user.name)

bot_commands.init(bot)

if __name__ == "__main__":
    bot.run(bot_key)
