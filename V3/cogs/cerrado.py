import discord
from discord.ext import commands
from datetime import datetime
import json

class CloseCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def load_data(self):
        try:
            with open('abierto.json', 'r') as file:
                data = json.load(file)
                # Convertir 'time_in' a datetime.datetime si es una cadena de texto
                for user_id, user_data in data.items():
                    if 'time_in' in user_data and isinstance(user_data['time_in'], str):
                        data[user_id]['time_in'] = datetime.fromisoformat(user_data['time_in'])
                return data
        except FileNotFoundError:
            return {}

    def save_data(self, data):
        with open('abierto.json', 'w') as file:
            json.dump(data, file, default=str)

    @commands.command()
    async def cerrado(self, ctx):
        await ctx.message.delete()
        user_id = str(ctx.author.id)
        data = self.load_data()
        
        # Verificar si alguno de los roles del usuario coincide con las IDs en el archivo JSON
        for role in ctx.author.roles:
            role_id = str(role.id)
            if role_id in data:
                time_in = data[role_id]['time_in']
                time_out = datetime.now()
                time_spent = time_out - time_in

                # Vaciar el valor de time_in
                data[role_id]['time_in'] = None

                # Si el usuario ya tiene un tiempo registrado, sumar el tiempo nuevo al existente
                if 'totald' in data[role_id]:
                    data[role_id]['totald'] += time_spent.days
                else:
                    data[role_id]['totald'] = time_spent.days
                    
                if 'totalh' in data[role_id]:
                    data[role_id]['totalh'] += time_spent.seconds // 3600  # Obtener las horas
                else:
                    data[role_id]['totalh'] = time_spent.seconds // 3600

                if 'totalm' in data[role_id]:
                    data[role_id]['totalm'] += (time_spent.seconds % 3600) // 60  # Obtener los minutos
                else:
                    data[role_id]['totalm'] = (time_spent.seconds % 3600) // 60

                if 'totals' in data[role_id]:
                    data[role_id]['totals'] += time_spent.seconds % 60  # Obtener los segundos
                else:
                    data[role_id]['totals'] = time_spent.seconds % 60

                # Guardar los datos actualizados
                self.save_data(data)

                days = str(data[role_id]['totald'])
                hours = str(data[role_id]['totalh'])
                minutes = str(data[role_id]['totalm'])
                seconds = str(data[role_id]['totals'])

                business_name = data[role_id]["empresa"]
                embed = discord.Embed(title=f'{business_name} esta cerrado',
                                    description=f'Tiempo transcurrido: {days}:{hours}:{minutes}:{seconds}.',
                                    color=discord.Color.red())
                await ctx.send(embed=embed)
                return  # Salir del bucle si se encuentra un rol válido
            
        # Si el usuario no tiene un rol válido
        await ctx.send('No has registrado tu entrada.')

def setup(bot):
    bot.add_cog(CloseCog(bot))
