from bot_utils import say


def init(bot, defaults):

    #pylint: disable=unused-variable
    # Bot commands go after this line.

    @bot.command(description="""Provide an invitation to the Performance
                                Analytics discord server.""")
    async def contact():

        result = "https://discord.gg/mJw8U4a"
        await say(bot, result, code_formatting=False)
    

    @bot.command(description="Display invite link for bot.")
    async def invite():

        await say(
            bot,
            ("https://discordapp.com/oauth2/authorize?client_id=48842402"
             "6591592461")
        )
    

    @bot.command(description="""Link Dr. Steven Gundry's 'The Plant Paradox'
                                Shopping List.""")
    async def lectin_list():

        await say(
            bot,
            ("https://gundrymd.com/wp-content/pdf/Plant-Paradox-Shopping-LIst."
             "pdf"),
            code_formatting=False
        )
    

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
