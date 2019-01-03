# -*- coding: utf-8 -*-
"""
Bot command definitions.
"""

from typing import Optional

import math

from performance_utils.formulas import Formula, Brzycki, Epley, McGlothin
from performance_utils.formulas import Lombardi, Mayhew, OConner, Wathan
import performance_utils.datatypes as T

from bot_utils import pendular_apply, say
import pstd.pstd.pickling as pstdpickling
import pstd.pstd.sessions as pstdsessions


def init(bot):
    """
    Initializes the module.
    
    This must be called in order to initialize commands.

    Args:
        bot: The bot object that commands should be registered to.
    """

    default_formula: str = "Epley"
    formula_dict = {
        "Brzycki": Brzycki,
        "Epley": Epley,
        "McGlothin": McGlothin,
        "Lombardi": Lombardi,
        "Mayhew": Mayhew,
        "O'Conner": OConner,
        "Wathan": Wathan,
    }

    #pylint: disable=unused-variable
    # Bot commands go after this line.

    @bot.command(description="Reverse Polish Notation calculator.")
    async def calc(*instructions):

        formula_class: Formula = formula_dict[default_formula]

        try:
            stack = []
            for instruction in instructions:
                if instruction.startswith("math."):
                    fn = getattr(math, instruction[5:])
                    stack.append(pendular_apply(fn, *reversed(stack)))
                elif instruction == "+":
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
                elif instruction == "del":
                    stack.pop()
                elif instruction == "sum":
                    stack = [sum(stack)]
                elif instruction == "product":
                    result = 1
                    for element in stack:
                        result *= element
                    stack = [result]
                elif instruction == "1rm":
                    arg2, arg1 = stack.pop(), stack.pop()
                    stack.append(formula_class.one_rep_max(arg2, arg1))
                elif instruction == "maxreps":
                    arg1 = stack.pop()
                    stack.append(formula_class.reps(arg1))
                elif instruction == "repmax":
                    arg2, arg1 = stack.pop(), stack.pop()
                    stack.append(formula_class.rep_max(arg1, arg2))
                else:
                    stack.append(float(instruction))
            await say(bot, "Result: {0}".format(stack.pop()))
        except:
            await say(bot, "Error.")


    @bot.command(description="""Display powerlifting classification information
                                for weightclasses (in kg, men only). If
                                `weight_class` is `0`, display available weight
                                classes. Available classification systems:
                                Russian.""")
    async def classes(weight_class: str = "0",
                      system: str = "Russian"):

        classes = {
            "Russian": {
                "53": {
                    "(Sub)Junior Class III": 195.0,
                    "(Sub)Junior Class II": 215.0,
                    "(Sub)Junior Class I": 232.5,
                    "Class III": 260.0,
                    "Class II": 282.5,
                    "Class I": 325.0,
                    "Candidate Master of Sport": 410.0
                },
                "59": {
                    "(Sub)Junior Class III": 212.5,
                    "(Sub)Junior Class II": 240.0,
                    "(Sub)Junior Class I": 260.0,
                    "Class III": 290.0,
                    "Class II": 315.0,
                    "Class I": 362.5,
                    "Candidate Master of Sport": 455.0,
                    "Master of Sport": 570.0,
                    "Master of Sport, International Class": 625.0
                },
                "66": {
                    "(Sub)Junior Class III": 227.5,
                    "(Sub)Junior Class II": 257.5,
                    "(Sub)Junior Class I": 287.5,
                    "Class III": 320.0,
                    "Class II": 350.0,
                    "Class I": 402.5,
                    "Candidate Master of Sport": 510.0,
                    "Master of Sport": 635.0,
                    "Master of Sport, International Class": 700.0
                },
                "74": {
                    "(Sub)Junior Class III": 247.5,
                    "(Sub)Junior Class II": 280.0,
                    "(Sub)Junior Class I": 317.5,
                    "Class III": 352.5,
                    "Class II": 385.0,
                    "Class I": 440.0,
                    "Candidate Master of Sport": 537.5,
                    "Master of Sport": 695.0,
                    "Master of Sport, International Class": 770.0
                },
                "83": {
                    "(Sub)Junior Class III": 277.5,
                    "(Sub)Junior Class II": 307.5,
                    "(Sub)Junior Class I": 352.5,
                    "Class III": 387.5,
                    "Class II": 422.5,
                    "Class I": 482.5,
                    "Candidate Master of Sport": 582.5,
                    "Master of Sport": 747.5,
                    "Master of Sport, International Class": 835.0
                },
                "93": {
                    "(Sub)Junior Class III": 307.5,
                    "(Sub)Junior Class II": 340.0,
                    "(Sub)Junior Class I": 382.5,
                    "Class III": 412.5,
                    "Class II": 465.0,
                    "Class I": 520.0,
                    "Candidate Master of Sport": 610.0,
                    "Master of Sport": 787.5,
                    "Master of Sport, International Class": 880.0
                },
                "105": {
                    "(Sub)Junior Class III": 330.0,
                    "(Sub)Junior Class II": 355.0,
                    "(Sub)Junior Class I": 397.5,
                    "Class III": 460.0,
                    "Class II": 500.0,
                    "Class I": 552.5,
                    "Candidate Master of Sport": 645.0,
                    "Master of Sport": 815.0,
                    "Master of Sport, International Class": 920.0
                },
                "120": {
                    "(Sub)Junior Class III": 347.5,
                    "(Sub)Junior Class II": 372.5,
                    "(Sub)Junior Class I": 422.5,
                    "Class III": 497.5,
                    "Class II": 530.0,
                    "Class I": 600.0,
                    "Candidate Master of Sport": 687.5,
                    "Master of Sport": 835.0,
                    "Master of Sport, International Class": 955.0
                },
                "120+": {
                    "(Sub)Junior Class III": 372.5,
                    "(Sub)Junior Class II": 390.0,
                    "(Sub)Junior Class I": 455.0,
                    "Class III": 510.0,
                    "Class II": 545.0,
                    "Class I": 617.5,
                    "Candidate Master of Sport": 735.0,
                    "Master of Sport": 860.0,
                    "Master of Sport, International Class": 980.0
                }
            }
        }

        try:
            result_system = classes[system]
            
            if weight_class == "0":
                await say(bot,
                          "# {0}\n- {1}".format(system,
                                            "\n- ".join([weight for weight
                                                       in result_system])),
                          syntax_highlight="markdown")
            else:
                try:
                    result = result_system[weight_class]
                    await say(
                        bot,
                        "# {0}\n- {1}".format(
                            weight_class,
                            "\n- ".join(
                                ["{0}: {1}".format(
                                    classification,
                                    result[classification]
                                ) for classification in result]
                            )
                        ),
                        syntax_highlight="markdown"
                    )
                except KeyError:
                    await say(bot, "Invalid weight class.")
        except KeyError:
            await say(bot, "Invalid classification system.")


    @bot.command(description="""Provide an invitation to the Performance
                                Analytics discord server.""")
    async def contact():

        result = "https://discord.gg/kZmsCrx"
        await say(bot, result, code_formatting=False)


    @bot.command(description="Show one-rep maximum formulas available.")
    async def formulas():

        result = ", ".join([name for name in formula_dict])
        await say(bot, "Formulas available: {0}".format(result))


    @bot.command(description="Calculate Fatigue-Variability Product.")
    async def fvp(inol: T.INOL, req: T.REQ):

        result = inol * req
        await say(bot, "FVP: {0:%} [{0}]".format(result))


    @bot.command(description="Calculate Intensity * Number Of Lifts.")
    async def inol(reps: T.Quantity, intensity: T.Intensity):

        result = reps / ((1 - intensity) * 100)
        await say(bot, "INOL: {0}".format(result))


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


    @bot.command(description="""Display volume landmarks suggested by Dr. Mike
                                Israetel's Hypertrophy Guides alongside a link
                                to the blog post.""")
    async def landmarks(muscle: str = None):

        muscle_groups = {
            "Pectoralis": {
                "MV": 8,
                "MEV": 10,
                "MAV Minimum": 12,
                "MAV Maximum": 20,
                "MRV": 22,
                "Frequency Minimum": 1.5,
                "Frequency Maximum": 3,
                "Reps/Set Minimum": 8,
                "Reps/Set Maximum": 12,
                "Hypertrophy Guide": ("https://renaissanceperiodization.com/ch"
                                      "est-training-tips-hypertrophy/")
            },
            "Tricep": {
                "MV": 4,
                "MEV": 6,
                "MAV Minimum": 10,
                "MAV Maximum": 14,
                "MRV": 18,
                "Frequency Minimum": 2,
                "Frequency Maximum": 4,
                "Reps/Set Minimum": 8,
                "Reps/Set Maximum": 20,
                "Hypertrophy Guide": ("https://renaissanceperiodization.com/tr"
                                      "iceps-hypertrophy-training-tips/")
            },
            "Bicep": {
                "MV": 5,
                "MEV": 8,
                "MAV Minimum": 14,
                "MAV Maximum": 20,
                "MRV": 26,
                "Frequency Minimum": 2,
                "Frequency Maximum": 6,
                "Reps/Set Minimum": 8,
                "Reps/Set Maximum": 15,
                "Hypertrophy Guide": ("https://renaissanceperiodization.com/bi"
                                      "cep-training-tips-hypertrophy/")
            },
            "Deltoid - Anterior": {
                "MV": 0,
                "MEV": 0,
                "MAV Minimum": 6,
                "MAV Maximum": 8,
                "MRV": 12,
                "Frequency Minimum": 2,
                "Frequency Maximum": 6,
                "Reps/Set Minimum": 10,
                "Reps/Set Maximum": 20,
                "Hypertrophy Guide": ("https://renaissanceperiodization.com/fr"
                                      "ont-delt-training-tips-hypertrophy/")
            },
            "Deltoid - Medial/Posterior": {
                "MV": 0,
                "MEV": 8,
                "MAV Minimum": 16,
                "MAV Maximum": 22,
                "MRV": 26,
                "Frequency Minimum": 2,
                "Frequency Maximum": 6,
                "Reps/Set Minimum": 10,
                "Reps/Set Maximum": 20,
                "Hypertrophy Guide": ("https://renaissanceperiodization.com/re"
                                      "arside-delt-tips-hypertrophy/")
            },
            "Trapezius": {
                "MV": 0,
                "MEV": 0,
                "MAV Minimum": 12,
                "MAV Maximum": 20,
                "MRV": 26,
                "Frequency Minimum": 2,
                "Frequency Maximum": 6,
                "Reps/Set Minimum": 10,
                "Reps/Set Maximum": 20,
                "Hypertrophy Guide": ("https://renaissanceperiodization.com/tr"
                                      "ap-training-tips-hypertrophy/")
            },
            "Back": {
                "MV": 8,
                "MEV": 10,
                "MAV Minimum": 14,
                "MAV Maximum": 22,
                "MRV": 25,
                "Frequency Minimum": 2,
                "Frequency Maximum": 4,
                "Reps/Set Minimum": 6,
                "Reps/Set Maximum": 20,
                "Hypertrophy Guide": ("https://renaissanceperiodization.com/ba"
                                      "ck-training-tips-hypertrophy/")
            },
            "Quadricep": {
                "MV": 6,
                "MEV": 8,
                "MAV Minimum": 12,
                "MAV Maximum": 18,
                "MRV": 20,
                "Frequency Minimum": 1.5,
                "Frequency Maximum": 3,
                "Reps/Set Minimum": 8,
                "Reps/Set Maximum": 15,
                "Hypertrophy Guide": ("https://renaissanceperiodization.com/qu"
                                      "ad-training-tips-hypertrophy/")
            },
            "Hamstring": {
                "MV": 4,
                "MEV": 6,
                "MAV Minimum": 10,
                "MAV Maximum": 16,
                "MRV": 20,
                "Frequency Minimum": 2,
                "Frequency Maximum": 3,
                "Reps/Set Minimum": 5,
                "Reps/Set Maximum": 15,
                "Hypertrophy Guide": ("https://renaissanceperiodization.com/ha"
                                      "mstring-training-tips-hyprtrophy/")
            },
            "Gluteus": {
                "MV": 0,
                "MEV": 0,
                "MAV Minimum": 4,
                "MAV Maximum": 12,
                "MRV": 16,
                "Frequency Minimum": 2,
                "Frequency Maximum": 3,
                "Reps/Set Minimum": 8,
                "Reps/Set Maximum": 12,
                "Hypertrophy Guide": ("https://renaissanceperiodization.com/gl"
                                      "ute-training-tips-hypertrophy/")
            },
            "Calf": {
                "MV": 6,
                "MEV": 8,
                "MAV Minimum": 12,
                "MAV Maximum": 16,
                "MRV": 20,
                "Frequency Minimum": 2,
                "Frequency Maximum": 4,
                "Reps/Set Minimum": 8,
                "Reps/Set Maximum": 15,
                "Hypertrophy Guide": ("https://renaissanceperiodization.com/ca"
                                      "lves-training-tips-hypertrophy/")
            },
            "Abdominals": {
                "MV": 0,
                "MEV": 0,
                "MAV Minimum": 16,
                "MAV Maximum": 20,
                "MRV": 25,
                "Frequency Minimum": 3,
                "Frequency Maximum": 5,
                "Reps/Set Minimum": 8,
                "Reps/Set Maximum": 20,
                "Hypertrophy Guide": ("https://renaissanceperiodization.com/ab"
                                      "-training/")
            }
        }

        if muscle is None:
            result = ("https://renaissanceperiodization.com/training-volume-la"
                      "ndmarks-muscle-growth/\n"
                      "https://renaissanceperiodization.com/hypertrophy-traini"
                      "ng-guide-central-hub/\n\n"
                      "Select from the following muscle groups:\n\n- {0}"
                      ).format("\n- ".join([muscle_group for muscle_group in
                                            muscle_groups]))
        else:
            result = "# {0}\n".format(muscle)
            muscle_group = muscle_groups[muscle]
            for item in muscle_group:
                result += "\n- {0}: {1}".format(item, muscle_group[item])
        await say(bot, result, syntax_highlight="markdown")


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


    @bot.command(description="""Link Dr. Steven Gundry's 'The Plant Paradox'
                                Shopping List.""")
    async def lectin_list():

        await say(
            bot,
            ("https://gundrymd.com/wp-content/pdf/Plant-Paradox-Shopping-LIst."
             "pdf"),
            code_formatting=False
        )


    @bot.command(description="""Calculate maximal repetition quantity from a
                                supplied percentage intensity.""")
    async def max_reps(intensity: T.Intensity, formula: str = default_formula):

        try:
            formula_class: Formula = formula_dict[formula]
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
                          formula: str = default_formula):

        try:
            formula_class: Formula = formula_dict[formula]
        except KeyError:
            await say(bot, "Formula name invalid.")
        else:
            result = formula_class.one_rep_max(reps, load)
            await say(bot, "One-Rep Max: {0}".format(result))


    @bot.command(description="Ping for a pong.")
    async def ping():

        await say(bot, "pong")


    @bot.command(pass_context=True,
                 description="Procedural Strength Training Director.")
    async def pstd(ctx,
                   fatigue_rating: str,
                   training_max: float):
        
        trainee = ctx.message.author.id
        training_cycle_name = "pa-bot pstd training cycle"
        iterator = pstdpickling.load_state(trainee, training_cycle_name)
        if iterator is None:
            iterator = pstdsessions.SessionBuilderCallbackIterator(
                pstdsessions.default_config
            )
        session_builder = next(iterator)
        session = session_builder(fatigue_rating, training_max)
        pstdpickling.save_state(iterator, trainee, training_cycle_name)
        volume_notation = "{}x{}".format(int(session.sets),
                                         int(session.reps_per_set))
        if session.extra_reps > 0:
            volume_notation += ", {}".format(session.extra_reps)
        await say(bot, "Volume: {}\nLoad: {}".format(volume_notation,
                                                     session.load))


    @bot.command(description="""Calculate maximal weight that can be moved for
                                supplied quantity of reps by a lifter with
                                specified one-rep max.""")
    async def rep_max(reps: int,
                      max: float,
                      formula: str = default_formula):
        
        try:
            formula_class: Formula = formula_dict[formula]
        except KeyError:
            await say(bot, "Formula name invalid.")
        else:
            result = formula_class.rep_max(reps, max)
            await say(bot, "{0} Repetition Maximum: {1}".format(reps, result))


    @bot.command(description="Calculate Repetition Endurance Quotient.")
    async def req(reps_performed: int, reps_possible: int):

        result = reps_performed / reps_possible
        await say(bot, "REQ: {0:.2%} [{0}]".format(result))


    @bot.command(description="Get Performance Analytics resources.")
    async def resources():

        await say(
            bot,
            ("https://drive.google.com/open?id=1Mk_Wutq9e0dh0Srm1KrDT9aNFlfdd7"
             "6G"),
            code_formatting=False
        )


    @bot.command(description="Link to bot source code.")
    async def source():

        await say(bot,
                "https://github.com/performance-analytics/pa-bot",
                code_formatting=False)


    @bot.command(description="Calculate Volume-Fatigue Index.")
    async def vfi(volume: float, inol: float):

        result = volume / inol
        await say(bot, "VFI: {0}".format(result))


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
            await say(bot, "Wilks ({0}): {1}".format(unit, result))
        except ZeroDivisionError:
            await say(bot, "Error: Division by zero.")
