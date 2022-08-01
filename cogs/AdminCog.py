import requests
from discord.ext import commands


class AdminCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def permission(self, ctx):
        await ctx.send('У вас есть права администратора.')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def authorize(self, ctx):
        req = requests.post("http://localhost:8080/submit_channel", json={"UUID": ctx.message.content.replace("*authorize", ""),
                                                                          "channelID": ctx.message.guild.id})
        await ctx.send(req.text)


def setup(bot):
    bot.add_cog(AdminCog(bot))
    print("Admin cog is active.")
