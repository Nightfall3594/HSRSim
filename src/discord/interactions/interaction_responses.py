from typing import Literal, Optional, Any

from pydantic import BaseModel
import httpx, os

from src.discord.interactions.component_message import ComponentMessage


class CallBackResponse(BaseModel):
    """
    Callback responses
    These are a set of methods for responding
    """

    @staticmethod
    def generic_message(message: str, interaction_id: str, token: str):
        """
        For sending your generic message responses.
        Bear in mind this uses the callback webhook
        """
        httpx.post(
            url=f"https://discord.com/api/v10/interactions/{interaction_id}/{token}/callback",
            headers={'Content-Type': 'application/json'},
            json={"type": 4, "data": {"content": message}}
        )


    @staticmethod
    def deferred_message(interaction_id: str, token: str):
        """
        For sending deferred messages.
        This sends a "bot is thinking..." response,
        and sending a follow-up to this message edits it
        """
        httpx.post(
            url=f"https://discord.com/api/v10/interactions/{interaction_id}/{token}/callback",
            headers={'Content-Type': 'application/json'},
            json={'type': 5}
        )



class FollowUpResponse(BaseModel):

    @staticmethod
    def send_followup(message: BaseModel, token: str):
        httpx.post(
            url=f"https://discord.com/api/v10/webhooks/{os.environ.get('APPLICATION_ID')}/{token}",
            headers={'Content-Type': 'application/json'},
            json= message.model_dump()
        )
