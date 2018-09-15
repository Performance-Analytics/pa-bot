#!/usr/bin/env python3

from discord.ext import commands
import math


bot = commands.Bot(command_prefix=",", description="Performance Analytics bot")


def say(message, syntax_highlight: str = ""):
    return bot.say("```{0}\n{1}\n```".format(syntax_highlight, message))


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
            else:
                stack.append(float(instruction))

        await say("Result: {0}".format(stack.pop()))

    except:

        await say("Error.")


@bot.command(description="Calculate Fatigue-Variability Product.")
async def fvp(inol: float, req: float):

    result = inol * req

    await say("FVP: {0:%} [{0}]".format(result))


@bot.command(description="Calculate Intensity * Number Of Lifts.")
async def inol(reps: int, intensity: float):

    result = reps / ((1 - intensity) * 100)

    await say("INOL: {0}".format(result))


@bot.command(description="""
    Calculate maximal repetition quantity from a supplied percentage intensity
    using Brzycki formula.
""")
async def max_reps(intensity: float):

    result = math.floor(37 - intensity * 36)

    await say("Maximum Reps: {0} @ {1:.2%} [{1}]".format(result, intensity))


@bot.command(description="""
    Calculate one-rep maximum weight from supplied load used and quantity of
    reps performed, using Brzycki formula.
""")
async def one_rep_max(load: float, reps: int):

    result = load * 36 / (37 - reps)

    await say("One-Rep Max: {0}".format(result))


@bot.command(description="Ping for a pong.")
async def ping():

    await say("pong")


@bot.command(description="""
    Calculate maximal weight that can be moved for supplied quantity of reps by
    a lifter with specified one-rep max, using Brzycki formula.
""")
async def rep_max(reps: int, max: float):

    result = max * (37 - reps) / 36

    await say("{0} Repetition Maximum: {1}".format(reps, result))


@bot.command(description="Calculate Repetition Endurance Quotient.")
async def req(reps_performed: int, reps_possible: int):

    result = reps_performed / reps_possible

    await say("REQ: {0:.2%} [{0}]".format(result))


@bot.command(description="Get Performance Analytics resources.")
async def resources():

    await say("https://drive.google.com/open?id=1Mk_Wutq9e0dh0Srm1KrDT9aNFlfdd76G")


@bot.command(description="Calculate Volume-Fatigue Index.")
async def vfi(volume: float, inol: float):

    result = volume / inol

    await say("VFI: {0}".format(result))


@bot.command(description="""
    Calculate Wilks score for supplied bodyweight and weight lifted.
""")
async def wilks(bodyweight: float, weight_lifted: float, kg: bool = True, male: bool = True):

    if male:
        a = -216.0475144
        b = 16.2606339
        c = -0.002388645
        d = -0.00113732
        e = 7.01863e-06
        f = -1.291e-08
    else:
        a = 594.31747775582
        b = -27.23842536447
        c = 0.82112226871
        d = -0.00930733913
        e = 4.731582e-05
        f = -9.054e-08

    if not kg:
        unit = "lb"
        weight_lifted /= 2.205
        bodyweight /= 2.205
    else:
        unit = "kg"

    try:

        coefficient = 500 / sum([
            a,
            b * bodyweight,
            c * (bodyweight ** 2),
            d * (bodyweight ** 3),
            e * (bodyweight ** 4),
            f * (bodyweight ** 5)
        ])
        result = coefficient * weight_lifted

        await say("Wilks ({0}): {1}".format(unit, result))

    except ZeroDivisionError:

        await say("Error: Division by zero.")


if __name__ == "__main__":
    bot.run("Enter bot key here.")
