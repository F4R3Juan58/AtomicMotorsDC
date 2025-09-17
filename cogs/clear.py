import discord
from discord.ext import commands

class ClearCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def clear(self, ctx, amount: int):
        """
        Elimina la cantidad especificada de mensajes del canal actual.
        """
        # Verificar si el autor del mensaje tiene permisos para eliminar mensajes
        if ctx.author.guild_permissions.manage_messages:
            # Eliminar los mensajes del canal actual
            await ctx.channel.purge(limit=amount + 1)  # +1 para incluir el propio mensaje de comando
        else:
            await ctx.send("No tienes permisos para eliminar mensajes.")

    # Añadir manejo de errores para el comando clear
    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Por favor, proporciona la cantidad de mensajes a eliminar.')
        elif isinstance(error, commands.BadArgument):
            await ctx.send('Por favor, proporciona un número entero válido.')
        else:
            await ctx.send('Se produjo un error al ejecutar el comando. Por favor, inténtalo de nuevo más tarde.')

def setup(bot):
    bot.add_cog(ClearCog(bot))
