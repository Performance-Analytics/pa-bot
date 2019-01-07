# -*- coding: utf-8 -*-
"""
Bot command definitions.
"""

import math

from performance_utils.formulas import Formula, Brzycki, Epley, McGlothin
from performance_utils.formulas import Lombardi, Mayhew, OConner, Wathan
import performance_utils.datatypes as T

from bot_utils import pendular_apply, say

import commands.conversion, commands.links, commands.parameters, commands.pstd
import commands.reference, commands.repmax, commands.util


def init(bot):
    """
    Initializes the module.
    
    This must be called in order to initialize commands.

    Args:
        bot: The bot object that commands should be registered to.
    """

    defaults = {
        "default_formula": "Epley",
        "formula_dict": {
            "Brzycki": Brzycki,
            "Epley": Epley,
            "McGlothin": McGlothin,
            "Lombardi": Lombardi,
            "Mayhew": Mayhew,
            "O'Conner": OConner,
            "Wathan": Wathan
        }
    }

    for module in [commands.conversion,
                   commands.links,
                   commands.parameters,
                   commands.pstd,
                   commands.reference,
                   commands.repmax,
                   commands.util]:
        module.init(bot, defaults)
