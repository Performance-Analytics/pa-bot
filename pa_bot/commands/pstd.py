import os, pprint

from bot_utils import say

import pstd.exceptions as pstdexceptions
import pstd.pickling as pstdpickling
import pstd.sessions as pstdsessions


def init(bot, defaults):

    #pylint: disable=unused-variable
    # Bot commands go after this line.

    @bot.command(pass_context=True,
                 description="""Procedural Strength Training Director. Fatigue
                                rating can be "low", "medium", or "high".
                                Training maxes are RPE 8 singles done before
                                the training session. Each training cycle
                                consists of only 1 exercise, so if you are
                                training multiple exercises you will need to
                                use a unique training cycle name for each.""")
    async def pstd(ctx,
                   fatigue_rating: str,
                   training_max: float,
                   training_cycle_name: str="default"):
        
        trainee = ctx.message.author.id
        iterator = pstdpickling.load_state(trainee, training_cycle_name)
        if iterator is None:
            iterator = pstdsessions.SessionBuilderCallbackIterator(
                pstdsessions.default_config
            )
        session_builder = next(iterator)
        try:
            session = session_builder(fatigue_rating, training_max)
        except pstdexceptions.InvalidFatigueRatingException as e:
            await say(bot, "Invalid fatigue rating `{}`.".format(e))
        else:
            pstdpickling.save_state(iterator, trainee, training_cycle_name)
            volume_notation = "{}x{}".format(int(session.sets),
                                            int(session.reps_per_set))
            if session.extra_reps > 0:
                volume_notation += ", {}".format(session.extra_reps)
            await say(bot, "Volume: {}\nLoad: {}".format(volume_notation,
                                                        session.load))
        

    @bot.command(pass_context=True,
                 description="""Create a custom configuration for a Procedural
                                Strength Training Director training cycle. Note
                                that this will overwrite any existing training
                                cycle with a new one, so be careful not to lose
                                important data.
                                
                                If no parameters are specified, a list of all
                                training cycle names will be shown.

                                If only the training cycle name is specified,
                                information about the requested training cycle
                                configuration will be displayed.""")
    async def pstdconfig(ctx,
                         training_cycle_name: str=None,
                         reps_per_set_small: int=None,
                         reps_per_set_medium: int=None,
                         reps_per_set_large: int=None,
                         inol_target_small: float=None,
                         inol_target_medium: float=None,
                         inol_target_large: float=None,
                         intensity_target_small: float=None,
                         intensity_target_medium: float=None,
                         intensity_target_large: float=None,
                         supramaximal_inol_increment: float=None):
    
        trainee = ctx.message.author.id

        # Query for all training cycle names.
        if training_cycle_name is None:
            try:
                # TODO: Move this try/except block's functionality to the
                # `pstd.pickling` module in the `pstd` package.
                training_cycles = os.listdir(pstdpickling.storage_path)
            except FileNotFoundError: # Storage path does not exist.
                training_cycles = []
            trainee_cycles = [
                "> {}".format(training_cycle[len(trainee):-len(".pickle")]) for
                training_cycle in
                training_cycles if
                training_cycle.startswith(trainee)
            ]
            await say(bot,
                      "# Training Cycles:\n{}".format(
                          "\n".join(trainee_cycles)
                      ),
                      syntax_highlight="markdown")

        # Query for details about a configuration.
        elif reps_per_set_small is None: # Only `training_cycle_name` is supplied.
            iterator = pstdpickling.load_state(trainee, training_cycle_name)
            if iterator is None:
                await say(bot, "Training cycle does not exist.")
            else:
                config = iterator.config
                await say(bot, pprint.pformat(config))
        
        else: # Create a new configuration.
            if reps_per_set_small is None:
                reps_per_set_small = pstdsessions.default_config[
                    "reps per set"
                ]["small"]
            if reps_per_set_medium is None:
                reps_per_set_medium = pstdsessions.default_config[
                    "reps per set"
                ]["medium"]
            if reps_per_set_large is None:
                reps_per_set_large = pstdsessions.default_config[
                    "reps per set"
                ]["large"]
            if inol_target_small is None:
                inol_target_small = pstdsessions.default_config[
                    "inol targets"
                ]["small"]
            if inol_target_medium is None:
                inol_target_medium = pstdsessions.default_config[
                    "inol targets"
                ]["medium"]
            if inol_target_large is None:
                inol_target_large = pstdsessions.default_config[
                    "inol targets"
                ]["large"]
            if intensity_target_small is None:
                intensity_target_small = pstdsessions.default_config[
                    "intensity targets"
                ]["small"]
            if intensity_target_medium is None:
                intensity_target_medium = pstdsessions.default_config[
                    "intensity targets"
                ]["medium"]
            if intensity_target_large is None:
                intensity_target_large = pstdsessions.default_config[
                    "intensity targets"
                ]["large"]
            if supramaximal_inol_increment is None:
                supramaximal_inol_increment = pstdsessions.default_config[
                    "supramaximal inol increment"
                ]

            config = {
                "reps per set": {
                    "small": reps_per_set_small,
                    "medium": reps_per_set_medium,
                    "large": reps_per_set_large
                },
                "inol targets": {
                    "small": inol_target_small,
                    "medium": inol_target_medium,
                    "large": inol_target_large
                },
                "intensity targets": {
                    "small": intensity_target_small,
                    "medium": intensity_target_medium,
                    "large": intensity_target_large
                },
                "supramaximal inol increment": supramaximal_inol_increment
            }
            iterator = pstdsessions.SessionBuilderCallbackIterator(config)
            pstdpickling.save_state(iterator, trainee, training_cycle_name)
            await say(bot, "Training cycle {} configured.".format(
                training_cycle_name
            ))


    @bot.command(pass_context=True,
                 description="""Deletes a Procedural Strength Training Director
                                training cycle. Take care when using this that
                                you do not delete any important information, as
                                it cannot be recovered afterward.""")
    async def pstdremove(ctx,
                         training_cycle_name="default"):

        trainee = ctx.message.author.id
        pickle_filename = "{}/{}{}.pickle".format(
            pstdpickling.storage_path,
            trainee,
            training_cycle_name
        )
        os.remove(pickle_filename)
        await say(bot, "Removed pickle {}".format(pickle_filename))