import discord
import config
from discord.ext import commands
from datetime import datetime
import json

class CloseCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def load_data(self):
        try:
            with open('json/empresas.json', 'r') as file:
                data = json.load(file)
                # Convertir 'time_in' a datetime.datetime si es una cadena de texto
                for user_id, user_data in data.items():
                    if 'time_in' in user_data and isinstance(user_data['time_in'], str):
                        data[user_id]['time_in'] = datetime.fromisoformat(user_data['time_in'])
                return data
        except FileNotFoundError:
            return {}

    def save_data(self, data):
        with open('json/empresas.json', 'w') as file:
            json.dump(data, file, default=str)

    async def notify_empresa_closed(self, empresa):
        channel = self.bot.get_channel(config.CHANNEL_ID)  # Obtener el canal desde la configuración
        data = self.load_data()
        
        # Verificar si la empresa está en los datos
        if empresa in data:
            time_in = data[empresa]['time_in']
            time_out = datetime.now()
            time_spent = time_out - time_in

            # Vaciar el valor de time_in
            data[empresa]['time_in'] = None

            # Si el usuario ya tiene un tiempo registrado, sumar el tiempo nuevo al existente
            if 'totald' in data[empresa]:
                data[empresa]['totald'] += time_spent.days
            else:
                data[empresa]['totald'] = time_spent.days
                
            if 'totalh' in data[empresa]:
                data[empresa]['totalh'] += time_spent.seconds // 3600  # Obtener las horas
            else:
                data[empresa]['totalh'] = time_spent.seconds // 3600

            if 'totalm' in data[empresa]:
                data[empresa]['totalm'] += (time_spent.seconds % 3600) // 60  # Obtener los minutos
            else:
                data[empresa]['totalm'] = (time_spent.seconds % 3600) // 60

            if 'totals' in data[empresa]:
                data[empresa]['totals'] += time_spent.seconds % 60  # Obtener los segundos
            else:
                data[empresa]['totals'] = time_spent.seconds % 60

            # Guardar los datos actualizados
            self.save_data(data)

            days = str(data[empresa]['totald'])
            hours = str(data[empresa]['totalh'])
            minutes = str(data[empresa]['totalm'])
            seconds = str(data[empresa]['totals'])

            embed = discord.Embed(title=f'{empresa} está cerrado',
                                  description=f'Tiempo transcurrido: {days}:{hours}:{minutes}:{seconds}.',
                                  color=discord.Color.red())
            await channel.send(embed=embed)
        else:
            await channel.send(f"No se encontró la empresa '{empresa}' en la base de datos.")

def setup(bot):
    bot.add_cog(CloseCog(bot))