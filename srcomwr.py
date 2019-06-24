import discord
from discord.ext import commands
import datetime
import srcomapi, srcomapi.datatypes as dt

api = srcomapi.SpeedrunCom()

class Mycog:
    """My custom cog that does stuff!"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def wr(self, ctx, gameName, catName):
        gameList = api.search(dt.Game, {"name": "{}".format(gameName)})
        worldRecord = ""
        if gameList:
            game = gameList[0]
            catName = catName.strip()
            curCategory = 0
            for category in game.categories:
                if str(category.name).lower() == str(catName).lower():
                    print(curCategory)
                    worldRecord = game.categories[curCategory].records[0].runs[0]["run"].times["primary_t"]
                    wrHolder = game.categories[curCategory].records[0].runs[0]["run"].players[0]
                curCategory = curCategory + 1

            if not worldRecord:
                strResp = "No record found for category {}".format(catName)
            else:
                strResp = "Current World Record for {} - {}  is: {} by {}".format(game.name, catName, str(datetime.timedelta(seconds=worldRecord)), wrHolder.name)
            
            await self.bot.say(strResp)
        else:
            await self.bot.say("Sorry, I couldn't find the game you're looking for.")

def setup(bot):
    bot.add_cog(Mycog(bot))

