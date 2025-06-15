from __future__ import annotations
from typing import Literal, Optional

import enka.models.hsr as hsr
from pydantic import BaseModel

from src.discord.components.message_components import *
from src.discord.constants.hsr_builds import STAT_EMOJIS, DMG_BONUSES


class ComponentMessage(BaseModel):
    """
    This is for a specific discord message type that uses components v2,
    and is different from your conventional discord message with embeds.
    """
    flags: Literal[32768] = 32768
    components: list[component_subclasses]


class BuildMessage(ComponentMessage):

    @classmethod
    def string_select(cls, options: list[StringSelectOption], custom_id: str):
        """
        Factory method for creating a simple string select layout.
        """
        str_select = StringSelectComponent(options=options, placeholder="Select a character", custom_id=custom_id)
        action_row = ActionRowComponent(components=[str_select])
        return cls(components=[action_row])


    @classmethod
    def build_showcase(cls, character: hsr.Character):
        """
        Factory method for the first page of an enka build character.
        """
        url = {'url': character.icon.card}
        image = MediaComponent.image(url=url)

        title = MessageComponent(content=f"# {character.name}")

        divider = MessageComponent(content=f"~~~                                                                            ~~~")

        stat_text = "\n\n".join(
            f"{STAT_EMOJIS[stat.name]} {stat.name}: {stat.formatted_value}"
            for stat in character.stats.values()
            if stat.name not in DMG_BONUSES and stat.value > 0
        )

        highest_dmg = character.highest_dmg_bonus_stat
        if highest_dmg.value > 0:
            stat_text += f"\n\n{STAT_EMOJIS[highest_dmg.name]} {highest_dmg.name}: {highest_dmg.formatted_value}"

        stat_message = MessageComponent(content=stat_text)

        container = ContainerComponent(components=[image, title, divider, stat_message], accent_color=9323909)
        final_message = cls(components=[container])

        return final_message



