# src/chatbot.py

import logging
from typing import List, Tuple
from .response_handler import ResponseHandler

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

class Chatbot:
    def __init__(self, response_handler: ResponseHandler):
        self.response_handler = response_handler
        self.history: List[Tuple[str, str]] = []

    async def get_response(self, user_input: str) -> str:
        logger.info(f"Received user input: '{user_input}'")
        response = await self.response_handler.get_response(user_input)
        self.history.append((user_input, response))
        logger.info(f"Responded with: '{response}'")
        return response

    def get_history(self) -> List[Tuple[str, str]]:
        return self.history

    def reset_history(self):
        self.history = []
        logger.info("Conversation history has been reset.")
