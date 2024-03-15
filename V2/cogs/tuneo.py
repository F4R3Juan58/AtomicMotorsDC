import discord
from discord.ext import commands
from datetime import datetime, timedelta
import json

class TuneoCog(commands.Cog):
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
    async def tuneo(self, ctx):
        """
        Solicita información sobre un vehículo y envía un embed con los detalles del tuneo.
        """
        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel

        # Solicitar información sobre el vehículo
        await ctx.send("Por favor, proporciona el nombre del vehículo:")
        vehicle_name = await self.bot.wait_for("message", check=check, timeout=60)

        await ctx.send("Por favor, proporciona la matrícula del vehículo:")
        license_plate = await self.bot.wait_for("message", check=check, timeout=60)

        await ctx.send("Por favor, proporciona el precio del tuneo:")
        price = await self.bot.wait_for("message", check=check, timeout=60)

        await ctx.send("Por favor, proporciona detalles sobre el tuneo realizado:")
        tuning_done = await self.bot.wait_for("message", check=check, timeout=60)

        # Obtener el número de tuneos realizados por el usuario
        user_id = str(ctx.author.id)
        tuneo_count = self.fichajes[user_id].get('tuneo_count', 0)
        
        # Incrementar el número de tuneos realizados por el usuario
        self.fichajes[user_id]['tuneo_count'] = tuneo_count + 1

        # Guardar los datos actualizados
        self.save_data(self.fichajes)

        # Construir el embed con la información proporcionada
        embed = discord.Embed(title=f"Tuneo realizado por {ctx.author.display_name} ({tuneo_count + 1} tuneos)",
                              color=discord.Color.green())
        embed.add_field(name="Nombre del vehículo", value=vehicle_name.content, inline=False)
        embed.add_field(name="Matrícula", value=license_plate.content, inline=False)
        embed.add_field(name="Precio", value=price.content, inline=False)
        embed.add_field(name="Tuneo realizado", value=tuning_done.content, inline=False)

        fake_message = ctx.message
        fake_message.content = f"!!clear {8}"

        # Procesar el comando
        await self.bot.process_commands(fake_message)
        
        # Enviar el embed al canal donde se ejecutó el comando
        message = await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(TuneoCog(bot))
