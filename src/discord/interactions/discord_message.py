from pydantic import BaseModel
import typing

class DiscordMessageContent(BaseModel):
    content: str

class DiscordMessage(BaseModel):
    type: typing.Literal[1, 4, 5, 6, 7, 8, 9]
    data: typing.Optional[DiscordMessageContent] = None

    @classmethod
    def generic_message(cls, text: str):
        return cls(type=4, data=DiscordMessageContent(content=text))

    @classmethod
    def deferred_message(cls, text: str):
        return cls(type=5, data=DiscordMessageContent(content=text))