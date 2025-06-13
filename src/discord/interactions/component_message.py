from __future__ import annotations
from typing import Literal, Optional

import enka.models.hsr as hsr
from pydantic import BaseModel

from src.discord.components.message_components import *


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

        stat_emojis = {
            "Outgoing Healing Boost": "<:OutgoingHealingBoost:1382674065378246716>",
            "Wind DMG Boost": "<:WindDMGBoost:1382674074907578379>",
            "SPD": "<:SPD:1382674190716637235>",
            "Quantum DMG Boost": "<:QuantumDMGBoost:1382674070054637660>",
            "Physical DMG Boost": "<:PhysicalDMGBoost:1382674067571871845>",
            "Lightning DMG Boost": "<:LightningDMGBoost:1382674063188693082>",
            "Imaginary DMG Boost": "<:ImaginaryDMGBoost:1382674060827426907>",
            "Ice DMG Boost": "<:IceDMGBoost:1382674058818093096>",
            "Fire DMG Boost": "<:FireDMGBoost:1382674054024265738>",
            "HP": "<:HP:1382674056679129188>",
            "Energy Regeneration Rate": "<:EnergyRegenerationRate:1382674051402829845>",
            "Effect RES": "<:EffectRES:1382674048471011338>",
            "Effect Hit Rate": "<:EffectHitRate:1382674046118006856>",
            "DEF": "<:DEF:1382674044041695262>",
            "CRIT Rate": "<:CRITRate:1382674042162516018>",
            "CRIT DMG": "<:CRITDMG:1382674039801122948>",
            "Break Effect": "<:BreakEffect:1382674037460701205>",
            "ATK": "<:ATK:1382674033648341154>"
        }

        url = {'url': character.icon.card}
        image = MediaComponent.image(url=url)

        title = MessageComponent(content=f"# {character.name}")

        divider = MessageComponent(content=f"~~~                                                                            ~~~")

        stat_text = ""

        for stat in character.stats.values():

            if stat.value != 0:
                stat_text = f"{stat_text}{stat_emojis[stat.name]} {stat.name}: {stat.formatted_value}\n\n"
        stat_message = MessageComponent(content=stat_text)

        container = ContainerComponent(components=[image, title, divider, stat_message], accent_color=9323909)
        final_message = cls(components=[container])

        return final_message



