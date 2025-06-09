from typing import Literal, Optional

import enka.models.hsr as hsr
from pydantic import BaseModel

from src.discord.components.message_components import *


class ComponentMessage(BaseModel):
    """
    This is for a specific discord message type that uses components like buttons,
    and is different from your conventional discord message with embeds.
    """
    flags: Literal[32678]
    components: list[component_subclasses]


class BuildMessage(ComponentMessage):

    @classmethod
    def string_select(cls, options: list[StringSelectOption]):
        """
        Factory method for creating a simple string select layout.
        """
        str_select = StringSelectComponent(type=3, options=options, placeholder="Select a character")
        action_row = ActionRowComponent(type=1, components=[str_select])
        return cls(flags=32678, components=[action_row])


    @classmethod
    def build_showcase(cls, character: hsr.Character):
        """
        Factory method for the first page of an enka build character.
        To do: add only raw stats, and an image.
        """
        pass