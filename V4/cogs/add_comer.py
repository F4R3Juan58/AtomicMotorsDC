import discord
from discord.ext import commands
import json
from datetime import datetime

class Addcomer(commands.Cog):
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

    @commands.command()
    async def add_comer(self, ctx, negocio_id: int,*,empresa: str):
        """
        Añade un usuario al fichero JSON con el ID de usuario y la empresa.
        """
        # Cargar los datos actuales del fichero JSON
        data = self.load_data()

        # Verificar si el usuario ya está en el fichero
        if str(negocio_id) in data:
            await ctx.send("El usuario ya está en el fichero.")
            return

        # Añadir el nuevo usuario al diccionario
        data[str(empresa)] = {
            'rol_id': negocio_id,
            'time_in': None,
            'time_out': None,
            'totald': 0,
            'totalh': 0,
            'totalm': 0,
            'totals': 0
        }

        # Guardar los datos actualizados en el fichero JSON
        self.save_data(data)

        await ctx.send(f"La empresa <@&{negocio_id}> se añadio de forma correcta.")

def setup(bot):
    bot.add_cog(Addcomer(bot))
