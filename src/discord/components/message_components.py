from __future__ import annotations
from typing import Literal, Union, Annotated, Optional

from pydantic import BaseModel, Field


class BaseComponent(BaseModel):
    type: int


class MessageComponent(BaseComponent):
    type: Literal[2]
    content: str


class ContainerComponent(BaseComponent):
    type: Literal[17]
    accent_color: Optional[int]
    components: list[component_subclasses]


class ActionRowComponent(BaseComponent):
    type: Literal[1]
    components: list[component_subclasses]


class StringSelectComponent(BaseComponent):
    type: Literal[3]
    placeholder: Optional[str]
    options: list[StringSelectOption]


class StringSelectOption(BaseModel):
    label: str
    value: str







component_subclasses = Annotated[Union[*BaseComponent.__subclasses__()], Field(discriminator="type")]

