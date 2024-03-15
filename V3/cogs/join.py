import discord
from discord.ext import commands
from datetime import datetime
import json

class JoinCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def load_data(self):
        try:
            with open('fichajes.json', 'r') as file:
                data = json.load(file)
                return data
        except FileNotFoundError:
            return {}

    def save_data(self, data):
        with open('fichajes.json', 'w') as file:
            json.dump(data, file, default=str)

    @commands.Cog.listener()
    async def on_ready(self):
        print('Bot is ready.')

    @commands.command()
    async def join(self, ctx):
        await ctx.message.delete()
        user = ctx.author
        user_id = str(user.id)
        data = self.load_data()
        if user_id in data:
            data[user_id]['time_in'] = datetime.now().isoformat()  # Actualizar solo el campo time_in
        else:
            data[user_id] = {'time_in': datetime.now().isoformat()}
        self.save_data(data)
        
        embed = discord.Embed(title=f'Bienvenido {user.display_name} al servicio.', color=discord.Color.green())
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(JoinCog(bot))
