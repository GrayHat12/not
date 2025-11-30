import bot.guild as guild
from bot.commands.common import ping
import discord
import logging
from discord.ext import commands
from commons.utils import get_module_name
from state import BotState, CommandIDMapping

state = BotState()


logger = logging.getLogger(get_module_name(__file__))

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(
    command_prefix="$",
    owner_id=state.Owner.Id,
    intents=intents,
)


@client.check
def allowed(ctx: commands.context.Context[commands.Bot]):
    # admin check
    if ctx.author.id == state.Owner.Id:
        return True

    # Allowed Channel/Commands Check
    allowed_channels = [*state.Owner.OwnerChannels]
    allowed_commands = []
    if ctx.guild and state.GuildConfigs[ctx.guild.id] and state.GuildConfigs[ctx.guild.id].BotAllowed:
        allowed_channels.extend(
            state.GuildConfigs[ctx.guild.id].AllowedChannels)
        allowed_commands.extend(
            state.GuildConfigs[ctx.guild.id].AllowedCommands)

    if ctx.guild and ctx.channel.id in allowed_channels and ctx.command and CommandIDMapping[ctx.command.name] in allowed_commands:
        return True
    return False


def update_command_ids():
    for command in client.commands:
        if "id" in command.extras and isinstance(command.extras["id"], int):
            CommandIDMapping[command.name] = command.extras["id"]
        else:
            command.enabled = False
    logger.debug(f"{CommandIDMapping=} after update")


@client.event
async def on_ready():
    update_command_ids()
    logger.info(f'Logged on as {client.user}!')


# @client.event
# async def on_message(message: discord.message.Message):
#     logger.info(
#         f'Message from {message.author.name}: {message.content} {message.channel} {message.guild}')

for export in guild.get_valid_event_listeners(guild):
    # logger.debug(f"Adding guild event listener {export.__name__}")
    client.event(export)


client.add_command(ping)
