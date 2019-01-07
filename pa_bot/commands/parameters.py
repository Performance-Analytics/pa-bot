from bot_utils import say

import performance_utils.datatypes as T


def init(bot, defaults):

    #pylint: disable=unused-variable
    # Bot commands go after this line.

    @bot.command(description="Calculate Fatigue-Variability Product.")
    async def fvp(inol: T.INOL, req: T.REQ):

        result = inol * req
        await say(bot, "FVP: {0:%} [{0}]".format(result))


    @bot.command(description="Calculate Intensity * Number Of Lifts.")
    async def inol(reps: T.Quantity, intensity: T.Intensity):

        result = reps / ((1 - intensity) * 100)
        await say(bot, "INOL: {0}".format(result))

    
    @bot.command(description="Calculate Repetition Endurance Quotient.")
    async def req(reps_performed: int, reps_possible: int):

        result = reps_performed / reps_possible
        await say(bot, "REQ: {0:.2%} [{0}]".format(result))


    @bot.command(description="Calculate Volume-Fatigue Index.")
    async def vfi(volume: float, inol: float):

        result = volume / inol
        await say(bot, "VFI: {0}".format(result))
