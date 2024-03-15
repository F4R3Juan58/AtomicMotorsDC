import discord
from discord.ext import commands
from datetime import timedelta
import json

class ResetCog(commands.Cog):
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

    def save_data(self, data):
        with open('fichajes.json', 'w') as file:
            json.dump(data, file, default=str)

    @commands.command()
    async def reset(self, ctx):
        for member_id in self.fichajes:
            self.fichajes[member_id]['total_time'] = timedelta()  # Reiniciar el tiempo a cero

        # Guardar los datos actualizados
        self.save_data(self.fichajes)

        await ctx.send('Se ha reiniciado el tiempo de trabajo de todos los miembros.')

def setup(bot):
    bot.add_cog(ResetCog(bot))
