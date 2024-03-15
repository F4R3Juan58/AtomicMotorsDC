import discord
from discord.ext import commands
from datetime import datetime
import json

class OpenCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def load_data(self):
        try:
            with open('abierto.json', 'r') as file:
                data = json.load(file)
                return data
        except FileNotFoundError:
            return {}

    def save_data(self, data):
        with open('abierto.json', 'w') as file:
            json.dump(data, file, default=str)

    @commands.command()
    async def abierto(self, ctx):
        await ctx.message.delete()
        data = self.load_data()

        user_id = ctx.author.id
        roles_ids = [str(role.id) for role in ctx.author.roles]

        # Verificar si alguno de los roles del usuario coincide con las IDs en el archivo JSON
        for role_id in roles_ids:
            if role_id in data:
                data[role_id]['time_in'] = datetime.now().isoformat()  # Actualizar solo el campo time_in
                business_name = data[role_id]["empresa"]  # Nombre del negocio asociado al ID del rol
                embed = discord.Embed(title=f"{business_name} está abierto", color=discord.Color.green())
                await ctx.send(embed=embed)
                self.save_data(data)  # Guardar los cambios en el JSON
                return

        # Si el usuario no tiene un rol válido
        embed = discord.Embed(title="No tienes permiso para usar este comando o no hay negocios abiertos", color=discord.Color.red())
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(OpenCog(bot))
