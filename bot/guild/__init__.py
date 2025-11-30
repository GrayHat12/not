import os
import discord
import logging
from typing import Sequence, ParamSpec, Any
from commons.utils import current_func_name
from inspect import iscoroutinefunction
from commons.error_handler import ModuleExceptionHandler
from exceptions.base import BaseBotException
from commons.decorator import task_decorator
from commons.utils import get_module_name

logger = logging.getLogger(get_module_name(__file__))

exception_handler = ModuleExceptionHandler(get_module_name(__file__))

P = ParamSpec('P')


async def _on_guild_event(event: str, *args, **kwargs):
    logger.info(f"got event {event} with {args=} {kwargs=}")
    # raise BaseBotException("meow meow mf")


@exception_handler.add_exception_handler(BaseBotException)
async def base_exception_handler(module: str, event: str, exception: BaseBotException, args: tuple[Any, ...], kwargs: dict[str, Any]):
    logger.error(
        f"{exception=} occured for {module=} {event=} with {args=} {kwargs=}"
    )


def get_valid_event_listeners(mod: object):
    for export_name in dir(mod):
        if export_name.startswith("on_"):
            export = getattr(mod, export_name, None)
            if export and callable(export) and iscoroutinefunction(export):
                yield export
    return None


@task_decorator(exception_handler, _on_guild_event)
async def on_guild_available(guild: discord.Guild):
    logger.info(f"got event {current_func_name()}")


@task_decorator(exception_handler, _on_guild_event)
async def on_guild_unavailable(guild: discord.Guild) -> None:
    logger.info(f"got event {current_func_name()}")


@task_decorator(exception_handler, _on_guild_event)
async def on_guild_join(guild: discord.Guild):
    logger.info(f"got event {current_func_name()}")


@task_decorator(exception_handler, _on_guild_event)
async def on_guild_remove(guild: discord.Guild):
    logger.info(f"got event {current_func_name()}")


@task_decorator(exception_handler, _on_guild_event)
async def on_guild_update(before: discord.Guild, after: discord.Guild):
    logger.info(f"got event {current_func_name()}")


@task_decorator(exception_handler, _on_guild_event)
async def on_guild_emojis_update(guild: discord.Guild, before: Sequence[discord.Emoji], after: Sequence[discord.Emoji]):
    logger.info(f"got event {current_func_name()}")


@task_decorator(exception_handler, _on_guild_event)
async def on_guild_stickers_update(guild: discord.Guild, before: Sequence[discord.GuildSticker], after: Sequence[discord.GuildSticker]):
    logger.info(f"got event {current_func_name()}")


@task_decorator(exception_handler, _on_guild_event)
async def on_audit_log_entry_create(entry: discord.AuditLogEntry):
    logger.info(f"got event {current_func_name()}")


@task_decorator(exception_handler, _on_guild_event)
async def on_invite_create(invite: discord.Invite):
    logger.info(f"got event {current_func_name()}")


@task_decorator(exception_handler, _on_guild_event)
async def on_invite_delete(invite: discord.Invite):
    logger.info(f"got event {current_func_name()}")
