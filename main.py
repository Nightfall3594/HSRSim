import pydantic
from fastapi import FastAPI, HTTPException
from starlette.requests import Request
from Discord.Commands import *
from Discord.SlashCommands import *

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
        # try:
        json = DiscordCommand(**json)

        # except pydantic.ValidationError as e:
        #     raise HTTPException(422, "Unprocessable Entity")

        context = DiscordContext(member=json.member)

        return json.data.execute(context)
