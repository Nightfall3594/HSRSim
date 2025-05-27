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
        try:
            json = DiscordCommand(**json)

        except pydantic.ValidationError as e:
            raise HTTPException(422, "Unprocessable Entity")

        context = DiscordContext(user=json.user, member=json.member)

        return json.data.execute(context) # assuming every single slash command implements execute()?

        # if isinstance(json.data, SlashGreet):
        #     output = {"type": 4, "data": {"content" : f"Hello, {json.member.user.username}. Would you like some cake?"}}
        #     return BotMessage(**output)
        #
        # if isinstance(json.data, SlashCalculateTurns):
        #
        #     speed = json.data.speed
        #     cycles = json.data.cycles
        #     turns = ((100 * cycles) + 50) // (10000/speed)
        #
        #     output = {"type": 4, "data": {"content": f"With a speed of {speed}, over the course of {cycles} cycles, a character would take {turns} turns"}}
        #     return BotMessage(**output)