from fastapi import FastAPI
from starlette.requests import Request

from DiscordCommands.PydanticModels import *

app = FastAPI()

@app.post('/api/discord')
async def discord(response: Request): #

    json = await response.json()

    if json.get("type") == 1:
        return {"type": 1}

    else:
        json = DiscordCommand(**json)
        if isinstance(json.data, SlashGreet):
            output = {"type": 4, "data": {"content" : f"Hello, {json.member.user.username}. Would you like some cake?"}}
            return BotMessage(**output)

        if isinstance(json.data, SlashCalculateTurns):

            speed = json.data.speed
            cycles = json.data.cycles
            turns = ((100 * cycles) + 50) // (10000/speed)

            output = {"type": 4, "data": {"content": f"With a speed of {speed}, over the course of {cycles} cycles, a character would take {turns} turns"}}
            return BotMessage(**output)