#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Entry point to bot.
"""


from typing import Optional
import math
import logging

from discord.ext import commands
from performance_utils.formulas import Formula, Brzycki, Epley, McGlothin
from performance_utils.formulas import Lombardi, Mayhew, OConner, Wathan
import performance_utils.datatypes as T


# Add bot key here.
bot_key: Optional[str] = None

# Debug logging mode?
debug: bool = False

if debug:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

bot = commands.Bot(command_prefix=",", description="Performance Analytics bot")

default_formula: str = "Brzycki"
formula_dict = {
    "Brzycki": Brzycki,
    "Epley": Epley,
    "McGlothin": McGlothin,
    "Lombardi": Lombardi,
    "Mayhew": Mayhew,
    "O'Conner": OConner,
    "Wathan": Wathan,
}


def say(message, code_formatting: bool = True, syntax_highlight: str = ""):

    if code_formatting:
        to_send = "```{0}\n{1}\n```".format(syntax_highlight, message)
    else:
        to_send = message
    return bot.say(to_send)


@bot.event
async def on_ready():

    print('Logged in as')
    print(bot.user.name)


@bot.command(description="Reverse Polish Notation calculator.")
async def calc(*instructions):

    try:
        stack = []
        for instruction in instructions:
            if instruction == "+":
                arg2, arg1 = stack.pop(), stack.pop()
                stack.append(arg1 + arg2)
            elif instruction == "-":
                arg2, arg1 = stack.pop(), stack.pop()
                stack.append(arg1 - arg2)
            elif instruction == "*":
                arg2, arg1 = stack.pop(), stack.pop()
                stack.append(arg1 * arg2)
            elif instruction == "/":
                arg2, arg1 = stack.pop(), stack.pop()
                stack.append(arg1 / arg2)
            elif instruction == "^":
                arg2, arg1 = stack.pop(), stack.pop()
                stack.append(arg1 ** arg2)
            elif instruction == "%":
                arg2, arg1 = stack.pop(), stack.pop()
                stack.append(arg1 % arg2)
            elif instruction == "abs":
                arg1 = stack.pop()
                stack.append(abs(arg1))
            elif instruction == "sum":
                stack = [sum(stack)]
            elif instruction == "product":
                result = 1
                for element in stack:
                    result *= element
                stack = [result]
            else:
                stack.append(float(instruction))
        await say("Result: {0}".format(stack.pop()))
    except:
        await say("Error.")


@bot.command(description="""Provides an invitation to the Performance Analytics
                            discord server.""")
async def contact():

    result = "https://discord.gg/kZmsCrx"
    await say(result, code_formatting=False)


@bot.command(description="Show one-rep maximum formulas available.")
async def formulas():

    result = ", ".join([name for name in formula_dict])
    await say("Formulas available: {0}".format(result))


@bot.command(description="Calculate Fatigue-Variability Product.")
async def fvp(inol: T.INOL, req: T.REQ):

    result = inol * req
    await say("FVP: {0:%} [{0}]".format(result))


@bot.command(description="Calculate Intensity * Number Of Lifts.")
async def inol(reps: T.Quantity, intensity: T.Intensity):

    result = reps / ((1 - intensity) * 100)
    await say("INOL: {0}".format(result))


@bot.command(description="""Convert imperial pounds (lb) to metric kilograms
                            (kg). If `rounding` is True, will round the result
                            to the nearest hundredth.""")
async def kg(lb: T.Load, rounding: bool = True):

    result = lb / 2.2046226218488

    if rounding:
        result_text = "{0:.2f}lb = {1:.2f}kg"
    else:
        result_text = "{0}lb = {1}kg"
    await say(result_text.format(lb, result))


@bot.command(description="""Convert metric kilograms (kg) to imperial pounds
                            (lb). If `rounding` is True, will round the result
                            to the nearest hundredth.""")
async def lb(kg: T.Load, rounding: bool = True):

    result = kg * 2.2046226218488

    if rounding:
        result_text = "{0:.2f}kg = {1:.2f}lb"
    else:
        result_text = "{0}kg = {1}lb"
    await say(result_text.format(kg, result))


@bot.command(description="""Link Dr. Steven Gundry's 'The Plant Paradox'
                            Shopping List.""")
async def lectin_list():

    await say(
        "https://gundrymd.com/wp-content/pdf/Plant-Paradox-Shopping-LIst.pdf",
        code_formatting=False
    )


@bot.command(description="""Calculate maximal repetition quantity from a
                            supplied percentage intensity.""")
async def max_reps(intensity: T.Intensity, formula: str = default_formula):

    try:
        formula_class: Formula = formula_dict[formula]
    except KeyError:
        await say("Formula name invalid.")
    else:
        result = math.floor(formula_class.reps(intensity))
        await say("Maximum Reps: {0} @ {1:.2%} [{1}]".format(result, intensity))


@bot.command(description="""Calculate one-rep maximum weight from supplied load
                            used and quantity of reps performed.""")
async def one_rep_max(load: float, reps: int, formula: str = default_formula):

    try:
        formula_class: Formula = formula_dict[formula]
    except KeyError:
        await say("Formula name invalid.")
    else:
        result = formula_class.one_rep_max(reps, load)
        await say("One-Rep Max: {0}".format(result))


@bot.command(description="Ping for a pong.")
async def ping():

    await say("pong")


@bot.command(description="""Calculate maximal weight that can be moved for
                            supplied quantity of reps by a lifter with
                            specified one-rep max.""")
async def rep_max(reps: int, max: float, formula: str = default_formula):
    
    try:
        formula_class: Formula = formula_dict[formula]
    except KeyError:
        await say("Formula name invalid.")
    else:
        result = formula_class.rep_max(reps, max)
        await say("{0} Repetition Maximum: {1}".format(reps, result))


@bot.command(description="Calculate Repetition Endurance Quotient.")
async def req(reps_performed: int, reps_possible: int):

    result = reps_performed / reps_possible
    await say("REQ: {0:.2%} [{0}]".format(result))


@bot.command(description="Get Performance Analytics resources.")
async def resources():

    await say(
        "https://drive.google.com/open?id=1Mk_Wutq9e0dh0Srm1KrDT9aNFlfdd76G",
        code_formatting=False
    )


@bot.command(description="Link to bot source code.")
async def source():

    await say("https://github.com/performance-analytics/pa-bot",
               code_formatting=False)


@bot.command(description="Calculate Volume-Fatigue Index.")
async def vfi(volume: float, inol: float):

    result = volume / inol
    await say("VFI: {0}".format(result))


@bot.command(description="""
    Calculate Wilks score for supplied bodyweight and weight lifted.
""")
async def wilks(bodyweight: float,
                weight_lifted: float,
                kg: bool = True,
                male: bool = True):

    if male:
        terms = [-216.0475144,
                 16.2606339,
                 -0.002388645,
                 -0.00113732,
                 7.01863e-06,
                 -1.291e-08]
    else:
        terms = [594.31747775582,
                 -27.23842536447,
                 0.82112226871,
                 -0.00930733913,
                 4.731582e-05,
                 -9.054e-08]

    if not kg:
        unit = "lb"
        weight_lifted /= 2.205
        bodyweight /= 2.205
    else:
        unit = "kg"

    try:
        new_terms = [term * (bodyweight ** power)
                     for (power, term)
                     in enumerate(terms)]
        coefficient = 500.0 / sum(new_terms)
        result = coefficient * weight_lifted
        await say("Wilks ({0}): {1}".format(unit, result))
    except ZeroDivisionError:
        await say("Error: Division by zero.")


if __name__ == "__main__":
    bot.run(bot_key)
