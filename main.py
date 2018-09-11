#!/usr/bin/env python3

from discord.ext import commands
import math


bot = commands.Bot(command_prefix=",", description="Performance Analytics bot")


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)


@bot.command(description="Calculate Fatigue-Variability Product.")
async def fvp(inol: float, req: float):
    result = inol * req
    await bot.say("FVP: {0:%} [{0}]".format(result))


@bot.command(description="Calculate Intensity * Number Of Lifts.")
async def inol(reps: int, intensity: float):
    result = reps / ((1 - intensity) * 100)
    await bot.say("INOL: {0}".format(result))


@bot.command(description="""
    Calculate maximal repetition quantity from a supplied percentage intensity
    using Brzycki formula.
""")
async def max_reps(intensity: float):
    result = math.floor(37 - intensity * 36)
    await bot.say("Maximum Reps: {0} @ {1:.2%} [{1}]".format(result, intensity))


@bot.command(description="""
    Calculate one-rep maximum weight from supplied load used and quantity of
    reps performed, using Brzycki formula.
""")
async def one_rep_max(load: float, reps: int):
    result = load * 36 / (37 - reps)
    await bot.say("One-Rep Max: {0}".format(result))


@bot.command(description="Ping for a pong.")
async def ping():
    await bot.say("pong")


@bot.command(description="""
    Calculate maximal weight that can be moved for supplied quantity of reps by
    a lifter with specified one-rep max, using Brzycki formula.
""")
async def rep_max(reps: int, max: float):
    result = max * (37 - reps) / 36
    await bot.say("{0} Repetition Maximum: {1}".format(reps, result))


@bot.command(description="Calculate Repetition Endurance Quotient.")
async def req(reps_performed: int, reps_possible: int):
    result = reps_performed / reps_possible
    await bot.say("REQ: {0:.2%} [{0}]".format(result))


@bot.command(description="Get Performance Analytics resources.")
async def resources():
    await bot.say("https://drive.google.com/open?id=1Mk_Wutq9e0dh0Srm1KrDT9aNFlfdd76G")


@bot.command(description="Calculate Volume-Fatigue Index.")
async def vfi(volume: float, inol: float):
    result = volume / inol
    await bot.say("VFI: {0}".format(result))


if __name__ == "__main__":
    bot.run("Enter bot key here.")
