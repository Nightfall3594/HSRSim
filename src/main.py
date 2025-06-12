from __future__ import  annotations

import json
import os
from typing import Annotated, Union

import pydantic
import uvicorn
from fastapi import FastAPI, HTTPException
from starlette.requests import Request
from starlette.responses import Response, JSONResponse
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError

from src.discord import DiscordContext, DiscordInteraction


app = FastAPI()

if not os.environ.get("PUBLIC_KEY"):
    os.environ["PUBLIC_KEY"] = input("Enter the bot public key: ")

if not os.environ.get("APPLICATION_ID"):
    os.environ["APPLICATION_ID"] = input("Enter the bot ID: ")


@app.get('/wake')
async def wake():
    return {"message": "MeiBot is awake!"}

@app.post('/api/discord')
async def discord(request: Request, response: Response): #

    body = await request.body()

    response.headers["User-Agent"] = "DiscordBot (https://meibot.onrender.com)"
    response.headers["Content-Type"] = "application/json"

    PUBLIC_KEY = os.environ.get("PUBLIC_KEY")

    verifier = VerifyKey(bytes.fromhex(PUBLIC_KEY))

    signature = request.headers["X-Signature-Ed25519"]
    timestamp = request.headers["X-Signature-Timestamp"]

    try:
        verifier.verify(timestamp.encode()+body, bytes.fromhex(signature))
    except BadSignatureError:
        return JSONResponse({"error": "Invalid signature"}, status_code=401)

    body = body.decode("utf-8")
    json_input = json.loads(body)

    if json_input.get("type") == 1:
        return JSONResponse({"type": 1}, status_code=200)

    else:
        print(json_input)

        adapter = pydantic.TypeAdapter(DiscordInteraction)
        #try:
        interaction = adapter.validate_python(json_input)

        #except pydantic.ValidationError as e:
            #raise HTTPException(422, "Unprocessable Entity")

        context = DiscordContext(member=interaction.member,
                                 interaction_token=interaction.token,
                                 interaction_id=interaction.id)

        return await interaction.data.execute(context)
