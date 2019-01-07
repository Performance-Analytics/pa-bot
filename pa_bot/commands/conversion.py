from bot_utils import say

import performance_utils.datatypes as T


def init(bot, defaults):

    #pylint: disable=unused-variable
    # Bot commands go after this line.

    @bot.command(description="""Convert imperial pounds (lb) to metric
                                kilograms (kg). If `rounding` is True, will
                                round the result to the nearest hundredth.""")
    async def kg(lb: T.Load, rounding: bool = True):

        result = lb / 2.2046226218488

        if rounding:
            result_text = "{0:.2f}lb = {1:.2f}kg"
        else:
            result_text = "{0}lb = {1}kg"
        await say(bot, result_text.format(lb, result))
    

    @bot.command(description="""Convert metric kilograms (kg) to imperial
                                pounds (lb). If `rounding` is True, will round
                                the result to the nearest hundredth.""")
    async def lb(kg: T.Load, rounding: bool = True):

        result = kg * 2.2046226218488

        if rounding:
            result_text = "{0:.2f}kg = {1:.2f}lb"
        else:
            result_text = "{0}kg = {1}lb"
        await say(bot, result_text.format(kg, result))
