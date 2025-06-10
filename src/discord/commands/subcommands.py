import typing
from typing import *

import enka.errors
from pydantic import BaseModel, Field
from enka import HSRClient
import httpx

from src.discord.commands import Options
from src.discord.components import DiscordContext
from src.discord.components.message_components import StringSelectOption
from src.discord.interactions.component_message import BuildMessage
from src.discord.interactions.interaction_responses import InteractionResponse

T = typing.TypeVar('T')

class SubCommand(BaseModel):
    name: str
    type: Literal[1]

    options: Optional[list[Options]] = None

    def _get(self, attribute: str, dtype: Type[T]) -> Optional[T]:
        if self.options:
            for i in self.options:
                if i.name == attribute:
                    return cast(dtype, i.value)

        return None


class CalculateTurns(SubCommand):
    name: Literal["turns"]

    @property
    def speed(self):
        return self._get("speed", float)


    @property
    def cycles(self):
        return self._get("cycles", int)


    def execute(self, context: DiscordContext):

        speed = self.speed
        cycles = self.cycles

        turns = ((100*cycles + 50) // (10000/speed))
        return InteractionResponse.generic_message(f"With a speed of {speed}, over the course of {cycles} cycle(s), a character would take {turns} turns")



class CalculateAV(SubCommand):

    name: Literal["av"]

    @property
    def speed(self):
        return self._get("speed", float)

    @property
    def action_advance(self):
        return self._get("action_advance", float)

    def execute(self, context: DiscordContext):

        action_gauge = (10000 * (1-self.action_advance))
        action_value = (action_gauge/self.speed)

        return InteractionResponse.generic_message(f"A character with a speed of {self.speed} and a {self.action_advance * 100}% action advance has an AV of {action_value}")


class ShowBuild(SubCommand):
    name: Literal["builds"]

    async def execute(self, ctx: DiscordContext):

        httpx.post(url=f"https://discord.com/api/v10/interactions/{ctx.interaction_id}/{ctx.interaction_token}/callback",
                   headers={'Content-Type': 'application/json'},
                   json={'type': 5})

        async with HSRClient() as client:
            try:
                response = await client.fetch_showcase(self.options[0].value)
            except enka.errors.RateLimitedError:
                return InteractionResponse.generic_message("Mmm, looks like you're hitting rate limits. How about you try again a few minutes from now?")

        if not response.characters:
            return InteractionResponse.generic_message("No characters found. Are you sure they are public?")

        char_list = []
        for character in response.characters:
            char_list.append(
                StringSelectOption(label=character.name, value=f"{self.options[0].value};{character.name}")
                )


        print("DEBUG-------------------------------------", flush=True)
        print("Endpoint: ", flush=True)
        print(f"https://discord.com/api/v10/webhooks/1375294904162451507/{ctx.interaction_token}", flush=True)
        print("\n\n\n", flush=True)
        print("Testcase payload", flush=True)
        print(BuildMessage.string_select(options=char_list, custom_id="character_select").model_dump(), flush=True)

        httpx.post(
            url=f"https://discord.com/api/v10/webhooks/1375294904162451507/{ctx.interaction_token}",
            headers={'Content-Type': 'application/json'},
            json=BuildMessage.string_select(options=char_list, custom_id="character_select").model_dump()
        )


        return None







subcommand_subclasses = Annotated[Union[*SubCommand.__subclasses__()], Field(discriminator="name")]