from discord.ext import commands
from discord.ext.commands.context import Context
from datetime import datetime, timezone
from commons.utils import get_module_name
import logging

logger = logging.getLogger(get_module_name(__file__))


@commands.command(name="ping", extras={"id": 0})
async def ping(ctx: Context):
    logger.info(f"got ping command")
    now = datetime.now(timezone.utc)
    latency = now - ctx.message.created_at
    await ctx.send(f"pong: latency={latency.microseconds / 1e3}ms")
