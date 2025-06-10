from __future__ import annotations
from typing import Literal, Optional

import enka.models.hsr as hsr
from pydantic import BaseModel

from src.discord.components.message_components import *


class ComponentMessage(BaseModel):
    """
    This is for a specific discord message type that uses components like buttons,
    and is different from your conventional discord message with embeds.
    """
    type: Literal[4] = 4
    data: ComponentMessageData


class ComponentMessageData(BaseModel):
    content: Optional[str] = None
    flags: Optional[int] = None
    components: list[component_subclasses]


class BuildMessage(ComponentMessage):

    @classmethod
    def string_select(cls, options: list[StringSelectOption], custom_id: str):
        """
        Factory method for creating a simple string select layout.
        """
        str_select = StringSelectComponent(type=3, options=options, placeholder="Select a character", custom_id=custom_id)
        action_row = ActionRowComponent(type=1, components=[str_select])
        data = ComponentMessageData(components=[action_row])
        return cls(data=data)


    @classmethod
    def build_showcase(cls, character: hsr.Character):
        """
        Factory method for the first page of an enka build character.
        """

        stat_emojis = {
            "Outgoing Healing Boost": "<:OutgoingHealingBoost:1379781408846778480>",
            "Wind DMG Boost": "<:WindDMGBoost:1379781382661996564>",
            "SPD": "<:SPD:1379781362512302173>",
            "Quantum DMG Boost": "<:QuantumDMGBoost:1379781344284114975>",
            "Physical DMG Boost": "<:PhysicalDMGBoost:1379781318702796840>",
            "Lightning DMG Boost": "<:LightningDMGBoost:1379781282132791437>",
            "Imaginary DMG Boost": "<:ImaginaryDMGBoost:1379781256773894254>",
            "Ice DMG Boost": "<:IceDMGBoost:1379781230429737040>",
            "Fire DMG Boost": "<:FireDMGBoost:1379781210850590810>",
            "HP": "<:HP:1379781167212924959>",
            "Energy Regeneration Rate": "<:EnergyRegenerationRate:1379781108618625137>",
            "Effect RES": "<:EffectRES:1379781081137549312>",
            "Effect Hit Rate": "<:EffectHitRate:1379781061105680587>",
            "DEF": "<:DEF:1379781034517729441>",
            "CRIT Rate": "<:CRITRate:1379781014838317147>",
            "CRIT DMG": "<:CRITDMG:1379780996718919710>",
            "Break Effect": "<:BreakEffect:1379780979492655185>",
            "ATK": "<:ATK:1379780949155254325>"
        }

        url = {'url': character.icon.card}
        image = MediaComponent(type=10, media=url)

        title = MessageComponent(type=2, content=f"{character.name}")

        divider = MessageComponent(type=2, content=f"~                                                                            ~")

        stats = [f"{stat_emojis[stat.name]}: {stat.formatted_value}\n\n" for stat in character.stats.values()]
        stat_text = ""
        for stat in stats:
            stat_text = stat_text+stat
        stat_message = MessageComponent(type=2, content=stat_text)

        container = ContainerComponent(type=17, components=[image, title, divider, stat_message], accent_color=9323909)
        data = ComponentMessageData(components=[container])
        final_message = cls(data=data)

        return final_message



