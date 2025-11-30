import os
import logging
from dataclasses import dataclass, field
from commons.utils import get_module_name, BidirectionalMap

logger = logging.getLogger(get_module_name(__file__))

CommandIDMapping: BidirectionalMap[str, int] = BidirectionalMap()
MonitoringIDMapping: BidirectionalMap[str, int] = BidirectionalMap()


@dataclass
class GuildConfig:
    BotPrefix: str = field(default_factory=lambda: "$")
    BotAllowed: bool = field(default_factory=lambda: False)
    AllowedCommands: list[int] = field(default_factory=lambda: [])
    GuildAdmins: list[int] = field(default_factory=lambda: [])
    MonitoringTypes: list[int] = field(default_factory=lambda: [])
    AllowedChannels: list[int] = field(default_factory=lambda: [])


@dataclass
class OwnerInfo:
    Id: int = field(default_factory=lambda: int(os.environ["OWNER_ID"]))
    OwnerServer: int = field(
        default_factory=lambda: int(os.environ["OWNER_SERVER"]))
    OwnerChannels: list[int] = field(
        default_factory=lambda: [int(channel) for channel in os.environ["OWNER_CHANNELS"].split(',')])
    AdminPrefix: str = field(default_factory=lambda: "$>")


@dataclass
class BotState:
    Owner: OwnerInfo = field(default_factory=lambda: OwnerInfo())
    GuildConfigs: dict[int, GuildConfig] = field(default_factory=lambda: {})
