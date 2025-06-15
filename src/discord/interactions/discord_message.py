from typing import Union, Literal, Optional, Any

from pydantic import BaseModel

from src.discord.components.discord_user import DiscordUser
from src.discord.components.message_components import *
from src.discord.component_commands.string_select_command import *


class DiscordMessage(BaseModel):
    """
    Represents a message object received from the Discord API.

    Attributes:
        id: The discord message ID
        channel_id: the channel id where the message is sent
        timestamp: the timestamp on the message in ISO format
        author: user object of the message author
        components: Different message components (distinct from ComponentsV2)
        content: the message content (in dict format)

    Note:
        When sending messages to discord, it's acceptable to leave the boilerplate blank.
        Discord will pre-fill those information for you.

    """
    id: Optional[str] = None
    channel_id: Optional[str] = None
    timestamp: Optional[str] = None
    author: Optional[DiscordUser] = None
    components: Optional[component_subclasses] = None
    content: dict[Literal["content"], str]

