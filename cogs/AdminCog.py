from discord.ext import commands


class AdminCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def permission(self, ctx):
        await ctx.send('У вас есть права администратора.')


def setup(bot):
    bot.add_cog(AdminCog(bot))
    print("Admin cog is active.")
