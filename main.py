
from typing import Union
import pydantic

from fastapi import FastAPI
from pydantic import BaseModel

import fastapi
from starlette.requests import Request

from PydanticModels import *

app = FastAPI()

# class CalculateCommand(BaseModel):
#
#     id: int
#     spd: float
#     cycles: int

# class DiscordResponse(BaseModel):
#
#     data: Union[CalculateCommand] = pydantic.Field(discriminator="id")


@app.post('/api/discord')
async def discord(response: Request): #

    json = await response.json()

    repr(json)

    if json.get("type") == 1:
        return {"type": 1}

    else:
        json = DiscordCommand(**json)
        if isinstance(json.data, SlashGreet):
            output = {"type": 4, "data": {"content" : f"Hello, {json.member.user.username}. Would you like some cake?"}}
            return BotMessage(**output)