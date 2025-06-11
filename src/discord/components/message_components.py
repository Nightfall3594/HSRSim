from __future__ import annotations
from typing import Literal, Union, Annotated, Optional

from pydantic import BaseModel, Field


class BaseComponent(BaseModel):
    type: int


class MessageComponent(BaseComponent):
    type: Literal[2] = 2
    content: str


class ContainerComponent(BaseComponent):
    type: Literal[17] = 17
    accent_color: Optional[int]
    components: list[component_subclasses]


class ActionRowComponent(BaseComponent):
    type: Literal[1] = 1
    components: list[component_subclasses]


class StringSelectComponent(BaseComponent):
    type: Literal[3] = 3
    placeholder: Optional[str] = None
    options: list[StringSelectOption]
    custom_id: str


class StringSelectOption(BaseModel):
    label: str
    value: str


class MediaComponent(BaseComponent):
    type: Literal[10] = 10
    media: dict
    description: Optional[str] = None







component_subclasses = Annotated[Union[*BaseComponent.__subclasses__()], Field(discriminator="type")]

