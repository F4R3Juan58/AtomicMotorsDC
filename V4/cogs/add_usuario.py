import discord
from discord.ext import commands
import json
from datetime import datetime

class Adduser(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def load_data(self):
        try:
            with open('json/fichajes.json', 'r') as file:
                data = json.load(file)
                return data
        except FileNotFoundError:
            return {}

    def save_data(self, data):
        with open('json/fichajes.json', 'w') as file:
            json.dump(data, file, default=str)

    @commands.command()
    async def add_user(self, ctx, user_id: int, *, empresa: str):
        """
        Añade un usuario al fichero JSON con el ID de usuario y la empresa.
        """
        # Cargar los datos actuales del fichero JSON
        data = self.load_data()

        # Verificar si el usuario ya está en el fichero
        if str(user_id) in data:
            await ctx.send("El usuario ya está en el fichero.")
            return

        # Añadir el nuevo usuario al diccionario
        data[str(user_id)] = {
            'empresa': empresa,
            'time_in': None,
            'tuneo_count': 0,
            'totald': 0,
            'totalh': 0,
            'totalm': 0,
            'totals': 0
        }

        # Guardar los datos actualizados en el fichero JSON
        self.save_data(data)

        await ctx.send(f"Usuario <@{user_id}> de la empresa {empresa} se añadio de forma correcta.")

def setup(bot):
    bot.add_cog(Adduser(bot))
