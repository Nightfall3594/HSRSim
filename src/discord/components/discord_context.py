from pydantic import BaseModel
import typing

from src.discord.components.discord_member import DiscordMember

class DiscordContext(BaseModel):
    member: typing.Optional[DiscordMember] = None