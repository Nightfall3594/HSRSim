from typing import Union, Literal, Optional, Any

from pydantic import BaseModel

from src.discord.components.discord_user import DiscordUser
from src.discord.components.message_components import *
from src.discord.component_commands.string_select_command import *


class SentMessage(BaseModel):
    id: str
    channel_id: str
    timestamp: str
    author: DiscordUser
    components: component_subclasses

