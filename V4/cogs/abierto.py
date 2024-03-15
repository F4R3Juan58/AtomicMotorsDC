import discord
import config
from discord.ext import commands
from datetime import datetime
import json

class OpenCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def load_data(self):
        try:
            with open('json/empresas.json', 'r') as file:
                data = json.load(file)
                return data
        except FileNotFoundError:
            return {}

    def save_data(self, data):
        with open('json/empresas.json', 'w') as file:
            json.dump(data, file, default=str)

    async def notify_empresa_open(self, empresa):
        channel = self.bot.get_channel(config.CHANNEL_ID)  # Obtener el canal desde la configuración

        if not channel:
            print(f"No se pudo encontrar el canal especificado en la configuración para notificar la apertura de {empresa}.")
            return

        data = self.load_data()

        if empresa in data:
            data[empresa]['time_in'] = datetime.now()  # Actualizar el tiempo de apertura de la empresa
            self.save_data(data)  # Guardar los cambios en el JSON
            embed = discord.Embed(title=f"{empresa} está abierto", color=discord.Color.green())
            await channel.send(embed=embed)  # Enviar el mensaje al canal
        else:
            await channel.send(f"No se encontró la empresa '{empresa}' en la base de datos.")

def setup(bot):
    bot.add_cog(OpenCog(bot))