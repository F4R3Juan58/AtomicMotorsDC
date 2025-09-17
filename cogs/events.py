import discord
from discord.ext import commands

class EventsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        # Aquí se puede agregar la lógica para cuando un miembro se une al servidor
        pass

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        # Aquí se puede agregar la lógica para cuando un miembro sale del servidor
        pass

def setup(bot):
    bot.add_cog(EventsCog(bot))
