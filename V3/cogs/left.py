import discord
from discord.ext import commands
from datetime import datetime, timedelta
import json
import config

class LeftCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def load_data(self):
        try:
            with open('fichajes.json', 'r') as file:
                data = json.load(file)
                # Convertir 'time_in' a datetime.datetime si es una cadena de texto
                for user_id, user_data in data.items():
                    if 'time_in' in user_data and isinstance(user_data['time_in'], str):
                        data[user_id]['time_in'] = datetime.fromisoformat(user_data['time_in'])
                return data
        except FileNotFoundError:
            return {}

    def save_data(self, data):
        with open('fichajes.json', 'w') as file:
            json.dump(data, file, default=str)

    @commands.command()
    async def left(self, ctx):
        await ctx.message.delete()
        user = ctx.author
        user_id = str(user.id)
        data = self.load_data()
        if user_id in data:
            time_in = data[user_id]['time_in']
            time_out = datetime.now()
            time_spent = time_out - time_in

            # Vaciar el valor de time_in
            data[user_id]['time_in'] = "null"

            # Si el usuario ya tiene un tiempo registrado, sumar el tiempo nuevo al existente
            if 'totald' in data[user_id]:
                data[user_id]['totald'] += time_spent.days
            else:
                data[user_id]['totald'] = time_spent.days
                
            if 'totalh' in data[user_id]:
                data[user_id]['totalh'] += time_spent.seconds // 3600  # Obtener las horas
            else:
                data[user_id]['totalh'] = time_spent.seconds // 3600

            if 'totalm' in data[user_id]:
                data[user_id]['totalm'] += (time_spent.seconds % 3600) // 60  # Obtener los minutos
            else:
                data[user_id]['totalm'] = (time_spent.seconds % 3600) // 60

            if 'totals' in data[user_id]:
                data[user_id]['totals'] += time_spent.seconds % 60  # Obtener los segundos
            else:
                data[user_id]['totals'] = time_spent.seconds % 60

            # Guardar los datos actualizados
            self.save_data(data)

            days = str(data[user_id]['totald'])
            hours = str(data[user_id]['totalh'])
            minutes = str(data[user_id]['totalm'])
            seconds = str(data[user_id]['totals'])
            
            embed = discord.Embed(title=f'{user.display_name} ha dejado el servicio',

                                color=discord.Color.red())
            await ctx.send(embed=embed)


            # Obtener el canal usando la ID del archivo de configuración
            channel = self.bot.get_channel(config.CHANNEL_ID)
            if channel is not None:
                embedp = discord.Embed(title=f'{user.display_name} ha dejado el servicio',
                                    description=f'Tiempo transcurrido: {days}:{hours}:{minutes}:{seconds}.',
                                    color=discord.Color.red())
                await channel.send(embed=embedp)
            else:
                await ctx.send("No se pudo encontrar el canal especificado en el archivo de configuración.")
            
        else:
            await ctx.send('No has registrado tu entrada.')

def setup(bot):
    bot.add_cog(LeftCog(bot))
