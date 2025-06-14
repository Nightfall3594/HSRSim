from typing import Literal, Optional

from pydantic import BaseModel

class DiscordMessageContent(BaseModel):
    content: str

class InteractionResponse(BaseModel):
    type: Literal[1, 4, 5, 6, 7, 8, 9]
    data: Optional[DiscordMessageContent] = None

    @classmethod
    def generic_message(cls, text: str):
        return cls(type=4, data=DiscordMessageContent(content=text))

    @classmethod
    def deferred_message(cls, text: str):
        return cls(type=5)
