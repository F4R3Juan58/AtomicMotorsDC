import discord
from discord.ext import commands
from datetime import timedelta
import json

class Stats_empresaCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.fichajes = self.load_data()

    def load_data(self):
        try:
            with open('json/fichajes.json', 'r') as file:
                data = json.load(file)
                # No es necesario convertir 'totald', 'totalh', 'totalm', 'totals' ya que ya están en formato adecuado
                return data
        except FileNotFoundError:
            return {}

    def cleanup_data(self, guild):
        for member_id in list(self.fichajes.keys()):
            if guild.get_member(int(member_id)) is None:
                del self.fichajes[member_id]

    @commands.command()
    async def stats_empresa(self, ctx, empresa: str):
        # Limpiar los datos de miembros ausentes en el servidor
        self.cleanup_data(ctx.guild)
        # Construir el embed
        embed = discord.Embed(title=f'Estadísticas de Fichajes - Empresa: {empresa}',
                              color=discord.Color.blue())

        # Recorrer todos los miembros y sus fichajes
        for member_id, data in self.fichajes.items():
            member_obj = ctx.guild.get_member(int(member_id))
            if member_obj and data.get('empresa') == empresa:  # Verificar si el miembro está en la empresa especificada
                total_days = data.get('totald', 0)
                total_hours = data.get('totalh', 0)
                total_minutes = data.get('totalm', 0)
                total_seconds = data.get('totals', 0)
                total_time = timedelta(days=total_days, hours=total_hours, minutes=total_minutes, seconds=total_seconds)
                embed.add_field(name=f'{member_obj.display_name} ({member_obj.top_role})',
                                value=f'Tiempo total: {total_time}',
                                inline=False)

        # Enviar el embed al canal donde se invocó el comando
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Stats_empresaCog(bot))
