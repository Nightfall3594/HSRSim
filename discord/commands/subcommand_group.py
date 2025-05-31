
from typing import Literal
from discord.base_classes import SubCommandGroup

class SampleSub1(SubCommandGroup):
    type: Literal[2]
    name: Literal["sample"]
