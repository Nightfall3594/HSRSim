from __future__ import annotations
from typing import Union, Optional, Annotated, Literal

from pydantic import BaseModel, Field
from enka import HSRClient

from src.discord.components import DiscordContext
from src.discord.interactions.component_message import BuildMessage
from src.discord.interactions.interaction_responses import *

class BaseStringSelectCommand(BaseModel):

    component_type: Literal[3]
    custom_id: str
    values: list[str]



class CharacterSelectCommand(BaseStringSelectCommand):
    """
    Bear in mind that self.values[0] is in the format {uid;character.name}.
    """
    custom_id: Literal["character_select"]

    @property
    def uid(self):
        return self.values[0].split(';')[0]

    @property
    def selection(self):
        return self.values[0].split(';')[1]

    async def execute(self, ctx: DiscordContext):
        async with HSRClient() as client:
            showcase = await client.fetch_showcase(self.uid)
            if showcase.characters:
                for char in showcase.characters:
                    if char.name == self.selection:
                        return BuildMessage.build_showcase(char)




string_select_subclasses = Annotated[Union[*BaseStringSelectCommand.__subclasses__()], Field(discriminator="custom_id")]