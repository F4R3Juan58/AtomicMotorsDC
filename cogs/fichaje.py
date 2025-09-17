import discord
from discord.ext import commands
from datetime import datetime, timedelta
import asyncio
import json
import config  # Importa el archivo de configuración

class FichajesCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.dataf = self.load_data('json/fichajes.json')
        self.datae = self.load_data('json/empresas.json')
        self.empresas_abiertas = {}  # Diccionario para rastrear el estado de cada empresa
        self.num_miembros_en_servicio = {}  # Diccionario para rastrear el número de miembros en servicio por empresa

    def load_data(self, filename):
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
                # Convertir 'time_in' a datetime.datetime si es una cadena de texto
                for user_id, user_data in data.items():
                    if 'time_in' in user_data and isinstance(user_data['time_in'], str):
                        data[user_id]['time_in'] = datetime.fromisoformat(user_data['time_in'])
                return data
        except FileNotFoundError:
            return {}

    def save_data(self, data, filename):
        with open(filename, 'w') as file:
            json.dump(data, file, default=str)

    async def update_empresa_state(self, empresa):
        # Actualizar el estado de la empresa
        if self.datae.get(empresa, {}).get("empleados_activos", 0) > 0:
            if not self.empresas_abiertas.get(empresa, False):
                self.empresas_abiertas[empresa] = True
                await self.bot.get_cog('OpenCog').notify_empresa_open(empresa)
        else:
            if self.empresas_abiertas.get(empresa, False):
                self.empresas_abiertas[empresa] = False
                await self.bot.get_cog('CloseCog').notify_empresa_closed(empresa)

    @commands.Cog.listener()
    async def on_ready(self):
        for empresa in self.datae.values():
            if empresa['empresa'] not in self.num_miembros_en_servicio:
                self.num_miembros_en_servicio[empresa['empresa']] = 0
        await self.update_all_empresa_states()

    async def update_all_empresa_states(self):
        # Actualizar el estado de todas las empresas
        for empresa in self.num_miembros_en_servicio.keys():
            await self.update_empresa_state(empresa)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        # Actualizar el estado de la empresa cuando un usuario sale del servidor
        empresa = self.dataf.get(str(member.id), {}).get('empresa', None)
        if empresa:
            self.num_miembros_en_servicio[empresa] -= 1
            await self.update_empresa_state(empresa)

    @commands.command()
    async def join(self, ctx):
        await ctx.message.delete()
        user_id = str(ctx.author.id)
        if user_id in self.dataf:
            empresa = self.dataf[user_id]['empresa'] 
            self.dataf[user_id]['time_in'] = datetime.now()
            self.save_data(self.dataf, 'json/fichajes.json')
            if empresa in self.datae:
                self.datae[empresa]['empleados_activos'] += 1  
                self.save_data(self.datae, 'json/empresas.json')
            else:
                await ctx.send("La empresa no es válida")

            # Notificar al usuario
            await ctx.send(f'Bienvenido {ctx.author.display_name} al servicio de {empresa}.')
            # Actualizar el estado de la empresa
            await self.update_empresa_state(empresa)
        else:
            await ctx.send('No has registrado tu entrada.')

    @commands.command()
    async def left(self, ctx):
        await ctx.message.delete()
        user_id = str(ctx.author.id)
        empresa = self.dataf.get(user_id, {}).get('empresa', None)
        if user_id in self.dataf:
            time_in = self.dataf[user_id]['time_in']
            time_out = datetime.now()
            time_spent = time_out - time_in

            # Calcular el tiempo transcurrido y actualizar los datos del usuario
            total_seconds = time_spent.total_seconds()
            self.dataf[user_id]['time_in'] = None
            if empresa in self.datae:
                self.datae[empresa]['empleados_activos'] -= 1  
                self.save_data(self.datae, 'json/empresas.json')
            # Agregar el tiempo transcurrido a los campos separados
            self.dataf[user_id].setdefault('totald', 0)
            self.dataf[user_id].setdefault('totalh', 0)
            self.dataf[user_id].setdefault('totalm', 0)
            self.dataf[user_id].setdefault('totals', 0)
            self.dataf[user_id]['totald'] += int(total_seconds // (3600 * 24))
            self.dataf[user_id]['totalh'] += int((total_seconds // 3600) % 24)
            self.dataf[user_id]['totalm'] += int((total_seconds // 60) % 60)
            self.dataf[user_id]['totals'] += int(total_seconds % 60)
            # Guardar los datos actualizados
            self.save_data(self.dataf, 'json/fichajes.json')
            # Notificar al usuario
            await ctx.send(f'{ctx.author.display_name} ha dejado el servicio de {empresa}.')
            # Actualizar el estado de la empresa
            await self.update_empresa_state(empresa)
        else:
            await ctx.send('No has registrado tu entrada.')

def setup(bot):
    bot.add_cog(FichajesCog(bot))