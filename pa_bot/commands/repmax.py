import math

from bot_utils import say

from performance_utils.formulas import Formula
import performance_utils.datatypes as T


def init(bot, defaults):
    
    #pylint: disable=unused-variable
    # Bot commands go after this line.
    
    @bot.command(description="Show one-rep maximum formulas available.")
    async def formulas():

        result = ", ".join([name for name in defaults["formula_dict"]])
        await say(bot, "Formulas available: {0}".format(result))
    

    @bot.command(description="""Calculate maximal repetition quantity from a
                                supplied percentage intensity.""")
    async def max_reps(intensity: T.Intensity,
                       formula: str = defaults["default_formula"]):

        try:
            formula_class: Formula = defaults["formula_dict"][formula]
        except KeyError:
            await say(bot, "Formula name invalid.")
        else:
            result = math.floor(formula_class.reps(intensity))
            await say(
                bot,
                "Maximum Reps: {0} @ {1:.2%} [{1}]".format(result,intensity)
            )

    
    @bot.command(description="""Calculate one-rep maximum weight from supplied
                                load used and quantity of reps performed.""")
    async def one_rep_max(load: float,
                          reps: int,
                          formula: str = defaults["default_formula"]):

        try:
            formula_class: Formula = defaults["formula_dict"][formula]
        except KeyError:
            await say(bot, "Formula name invalid.")
        else:
            result = formula_class.one_rep_max(reps, load)
            await say(bot, "One-Rep Max: {0}".format(result))


    @bot.command(description="""Calculate maximal weight that can be moved for
                                supplied quantity of reps by a lifter with
                                specified one-rep max.""")
    async def rep_max(reps: int,
                      max: float,
                      formula: str = defaults["default_formula"]):
        
        try:
            formula_class: Formula = defaults["formula_dict"][formula]
        except KeyError:
            await say(bot, "Formula name invalid.")
        else:
            result = formula_class.rep_max(reps, max)
            await say(bot, "{0} Repetition Maximum: {1}".format(reps, result))


    @bot.command(description="""Calculate maximal weight that can be moved for
                                each quantity of reps between 1 and 10
                                (inclusive) by a lifter with specified one-rep
                                max.""")
    async def rep_maxes(max: float,
                        formula: str = defaults["default_formula"]):
        
        try:
            formula_class: Formula = defaults["formula_dict"][formula]
        except KeyError:
            await say(bot, "Formula name invalid.")
        else:
            result = "\n".join([
                "{:>2}RM: {:.2f}".format(reps,
                                  formula_class.rep_max(reps, max)) for
                reps in
                range(1, 11)
            ])
            await say(bot, result)
