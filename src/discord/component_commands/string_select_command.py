from __future__ import annotations
from typing import Union, Optional, Annotated, Literal
import os

from pydantic import BaseModel, Field
from enka import HSRClient
import httpx

from src.discord.components import DiscordContext
from src.discord.interactions.component_message import BuildMessage
from src.discord.interactions.interaction_responses import *

class BaseStringSelectCommand(BaseModel):

    component_type: Literal[3]
    custom_id: str
    values: list[str]


class CharacterSelectCommand(BaseStringSelectCommand):
    """
    Bear in mind that self.values[0] is in the format {uid;character.name}.
    """
    custom_id: Literal["character_select"]

    @property
    def uid(self):
        return self.values[0].split(';')[0]

    @property
    def selection(self):
        return self.values[0].split(';')[1]

    async def execute(self, ctx: DiscordContext):

        # defer the response
        CallBackResponse.deferred_message(ctx.interaction_id, ctx.interaction_token)

        async with HSRClient() as client:
            showcase = await client.fetch_showcase(self.uid)
            if showcase.characters:
                for char in showcase.characters:
                    if char.name == self.selection:

                        print("DEBUG: Logging endpoint:", flush=True)
                        print(f"Endpoint: https://discord.com/api/v10/webhooks/{os.environ.get('APPLICATION_ID')}/{ctx.interaction_token}", flush=True)
                        print(f"Payload: {BuildMessage.build_showcase(char).model_dump()}", flush=True)
                        print("\n\n\n", flush=True)

                        FollowUpResponse.send_followup(BuildMessage.build_showcase(char), ctx.interaction_token)




string_select_subclasses = Annotated[Union[*BaseStringSelectCommand.__subclasses__()], Field(discriminator="custom_id")]