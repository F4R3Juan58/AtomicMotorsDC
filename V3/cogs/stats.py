import discord
from discord.ext import commands
from datetime import timedelta
import json

class StatsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.fichajes = self.load_data()

    def load_data(self):
        try:
            with open('fichajes.json', 'r') as file:
                data = json.load(file)
                # Convertir 'total_time' a datetime.timedelta si es una cadena de texto
                for user_id, user_data in data.items():
                    if 'total_time' in user_data and isinstance(user_data['total_time'], str):
                        time_components = user_data['total_time'].split(':')
                        hours, minutes, seconds = map(float, time_components)
                        total_seconds = hours * 3600 + minutes * 60 + seconds
                        data[user_id]['total_time'] = timedelta(seconds=total_seconds)
                return data
        except FileNotFoundError:
            return {}

    def cleanup_data(self, guild):
        for member_id in list(self.fichajes.keys()):
            if guild.get_member(int(member_id)) is None:
                del self.fichajes[member_id]

    @commands.command()
    async def stats(self, ctx):
        # Limpiar los datos de miembros ausentes en el servidor
        self.cleanup_data(ctx.guild)

        # Construir el embed
        embed = discord.Embed(title='Estadísticas de Fichajes',
                              color=discord.Color.blue())

        # Recorrer todos los miembros y sus fichajes
        for member_id, data in self.fichajes.items():
            member_obj = ctx.guild.get_member(int(member_id))
            if member_obj:  # Verificar si el miembro aún está en el servidor
                total_time = data.get('total_time', timedelta())
                embed.add_field(name=f'{member_obj.display_name} ({member_obj.top_role})',
                                value=f'Tiempo total: {total_time}',
                                inline=False)

        # Enviar el embed al canal donde se invocó el comando
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(StatsCog(bot))
