from bot_utils import say


def init(bot, defaults):

    #pylint: disable=unused-variable
    # Bot commands go after this line.

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
