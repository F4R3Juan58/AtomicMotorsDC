import discord
from discord.ext import commands
import json
import config
from datetime import datetime, timedelta
import asyncio

intents = discord.Intents.default()
intents.typing = False
intents.presences = False

bot = commands.Bot(command_prefix="!!", intents=discord.Intents.all())

# Función para cargar los datos desde un archivo JSON
def load_data():
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


# Función para guardar los datos en un archivo JSON
def save_data(data):
    with open('fichajes.json', 'w') as file:
        json.dump(data, file, default=str) 

# Función para limpiar los datos de miembros que ya no están en el servidor
def cleanup_data(guild):
    for member_id in list(fichajes.keys()):
        if guild.get_member(int(member_id)) is None:
            del fichajes[member_id]

fichajes = load_data()

@bot.event
async def on_ready():
    print('Bot is ready.')

@bot.command()
async def join(ctx):
    await ctx.message.delete()
    user = ctx.author
    if str(user.id) not in fichajes:
        fichajes[str(user.id)] = {'time_in': datetime.now().isoformat()}  # Convertir a ISO 8601
        save_data(fichajes)  # Guardar los datos actualizados
        embed = discord.Embed(title=f'Bienvenido {user.display_name} al servicio.', color=discord.Color.green())
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title=f'Bienvenido {user.display_name} al servicio.', color=discord.Color.green())
        await ctx.send(embed=embed)

@bot.command()
async def left(ctx):
    await ctx.message.delete()
    user = ctx.author
    user_id = str(user.id)
    if user_id in fichajes:
        time_in = datetime.fromisoformat(fichajes[user_id]['time_in'])
        time_out = datetime.now()
        time_spent = time_out - time_in

        # Si el usuario ya tiene un tiempo registrado, sumar el tiempo nuevo al existente
        if 'total_time' in fichajes[user_id]:
            fichajes[user_id]['total_time'] += time_spent
        else:
            fichajes[user_id]['total_time'] = time_spent

        # Guardar los datos actualizados
        save_data(fichajes)

        # Convertir la duración del tiempo a una cadena de texto legible
        time_spent_json = fichajes[user_id].get('total_time', timedelta())  # Obtener el tiempo transcurrido del fichero JSON

        # Convertir el tiempo transcurrido a una cadena de texto legible
        days = time_spent_json.days
        hours, remainder = divmod(time_spent_json.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        time_spent_str = f"{days} días, {hours} horas, {minutes} minutos y {seconds} segundos"

        # Construir el embed
        embed = discord.Embed(title=f'{user.display_name} ha dejado el servicio',
                              description=f'Ha estado en servicio durante {time_spent_str}.',
                              color=discord.Color.red())
        await ctx.send(embed=embed)
        
        # Enviar el embed al canal deseado
        channel_id = config.CHANNEL_ID  # Reemplaza con el ID del canal deseado
        channel = bot.get_channel(channel_id)
        await channel.send(embed=embed)
    else:
        await ctx.send('No has registrado tu entrada.')


@bot.command()
async def tuneo(ctx):
    """
    Solicita información sobre un vehículo y envía un embed con los detalles del tuneo.
    """
    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel

    # Solicitar información sobre el vehículo
    await ctx.send("Por favor, proporciona el nombre del vehículo:")
    vehicle_name = await bot.wait_for("message", check=check, timeout=60)

    await ctx.send("Por favor, proporciona la matrícula del vehículo:")
    license_plate = await bot.wait_for("message", check=check, timeout=60)

    await ctx.send("Por favor, proporciona el precio del tuneo:")
    price = await bot.wait_for("message", check=check, timeout=60)

    await ctx.send("Por favor, proporciona detalles sobre el tuneo realizado:")
    tuning_done = await bot.wait_for("message", check=check, timeout=60)

    # Obtener el número de tuneos realizados por el usuario
    user_id = str(ctx.author.id)
    tuneo_count = fichajes[user_id].get('tuneo_count', 0)
    
    # Incrementar el número de tuneos realizados por el usuario
    fichajes[user_id]['tuneo_count'] = tuneo_count + 1

    # Guardar los datos actualizados
    save_data(fichajes)

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
    await bot.process_commands(fake_message)
    
    # Enviar el embed al canal donde se ejecutó el comando
    message = await ctx.send(embed=embed)

@bot.command()
async def stats(ctx):
    # Limpiar los datos de miembros ausentes en el servidor
    cleanup_data(ctx.guild)

    # Construir el embed
    embed = discord.Embed(title='Estadísticas de Fichajes',
                          color=discord.Color.blue())

    # Recorrer todos los miembros y sus fichajes
    for member_id, data in fichajes.items():
        member_obj = ctx.guild.get_member(int(member_id))
        if member_obj:  # Verificar si el miembro aún está en el servidor
            total_time = data.get('total_time', 0)
            embed.add_field(name=f'{member_obj.display_name} ({member_obj.top_role})',
                            value=f'Tiempo total: {total_time}',
                            inline=False)

    # Enviar el embed al canal donde se invocó el comando
    await ctx.send(embed=embed)

@bot.command()
async def reset(ctx):
    for member_id in fichajes:
        fichajes[member_id]['total_time'] = datetime.timedelta()  # Reiniciar el tiempo a cero

    # Guardar los datos actualizados
    save_data(fichajes)

    await ctx.send('Se ha reiniciado el tiempo de trabajo de todos los miembros.')

@bot.command()
async def clear(ctx, amount: int):
    """
    Elimina la cantidad especificada de mensajes del canal actual.
    """
    # Verificar si el autor del mensaje tiene permisos para eliminar mensajes
    if ctx.author.guild_permissions.manage_messages:
        # Eliminar los mensajes del canal actual
        await ctx.channel.purge(limit=amount + 1)  # +1 para incluir el propio mensaje de comando
    else:
        await ctx.send("No tienes permisos para eliminar mensajes.")

# Añadir manejo de errores para el comando clear
@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Por favor, proporciona la cantidad de mensajes a eliminar.')
    elif isinstance(error, commands.BadArgument):
        await ctx.send('Por favor, proporciona un número entero válido.')
    else:
        await ctx.send('Se produjo un error al ejecutar el comando. Por favor, inténtalo de nuevo más tarde.')

# Ejecutar la limpieza de datos al unirse o salir un miembro del servidor
@bot.event
async def on_member_join(member):
    cleanup_data(member.guild)

@bot.event
async def on_member_remove(member):
    cleanup_data(member.guild)

bot.run(config.TOKEN)
