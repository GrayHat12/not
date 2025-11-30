from bot.commands.common import ping
import discord
import logging
from discord.ext import commands
from commons.utils import get_module_name

import bot.guild as guild

logger = logging.getLogger(get_module_name(__file__))

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix="$", intents=intents)


@client.event
async def on_ready():
    logger.info(f'Logged on as {client.user}!')


# @client.event
# async def on_message(message: discord.message.Message):
#     logger.info(
#         f'Message from {message.author.name}: {message.content} {message.channel} {message.guild}')

for export in guild.get_valid_event_listeners(guild):
    # logger.debug(f"Adding guild event listener {export.__name__}")
    client.event(export)


client.add_command(ping)
