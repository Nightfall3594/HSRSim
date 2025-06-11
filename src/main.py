from __future__ import  annotations

from typing import Annotated, Union

import pydantic
import uvicorn
from fastapi import FastAPI, HTTPException
from starlette.requests import Request

from src.discord import DiscordContext, DiscordInteraction


app = FastAPI()


@app.get('/wake')
async def wake():
    return {"message": "MeiBot is awake!"}

@app.post('/api/discord')
async def discord(response: Request): #

    json = await response.json()

    if json.get("type") == 1:
        return {"type": 1}

    else:

        print(json)

        adapter = pydantic.TypeAdapter(DiscordInteraction)
        #try:
        interaction = adapter.validate_python(json)

        #except pydantic.ValidationError as e:
            #raise HTTPException(422, "Unprocessable Entity")


        context = DiscordContext(member=interaction.member,
                                 interaction_token=interaction.token,
                                 interaction_id=interaction.id)

        return await interaction.data.execute(context)
