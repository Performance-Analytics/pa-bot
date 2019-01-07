import math

from performance_utils.formulas import Formula

from bot_utils import pendular_apply, say


def init(bot, defaults):

    #pylint: disable=unused-variable
    # Bot commands go after this line.

    @bot.command(description="Reverse Polish Notation calculator.")
    async def calc(*instructions):

        formula_class: Formula = defaults["formula_dict"][
            defaults["default_formula"]
        ]

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
                elif instruction == "inol":
                    arg2, arg1 = stack.pop(), stack.pop()
                    stack.append(arg1 / ((1 - arg2) * 100))
                else:
                    stack.append(float(instruction))
            await say(bot, "Result: {0}".format(stack.pop()))
        except:
            await say(bot, "Error.")


    @bot.command(description="Ping for a pong.")
    async def ping():

        await say(bot, "pong")


    @bot.command(description="""Calculate Wilks score for supplied bodyweight
                                and weight lifted.""")
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
