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
        image = MediaComponent.image(url=url)

        title = MessageComponent(content=f"# {character.name}")

        divider = MessageComponent(content=f"~~~                                                                            ~~~")

        stat_text = ""

        for stat in character.stats.values():

            if stat.value != 0:
                stat_text = f"{stat_text}{stat_emojis[stat.name]}{stat.name}: {stat.formatted_value}\n\n"
        stat_message = MessageComponent(content=stat_text)

        container = ContainerComponent(components=[image, title, divider, stat_message], accent_color=9323909)
        final_message = cls(components=[container])

        return final_message



