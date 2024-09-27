# tests/test_chatbot.py

import pytest
from unittest.mock import MagicMock
from src.chatbot import Chatbot

@pytest.fixture
def mock_response_handler():
    return MagicMock()

@pytest.mark.asyncio
async def test_get_response_predefined(mock_response_handler):
    async def mock_get_response(*args, **kwargs):
        return "Predefined answer."
        
    mock_response_handler.get_response.side_effect = mock_get_response
    chatbot = Chatbot(response_handler=mock_response_handler)
    response = await chatbot.get_response("What is AI?")
    assert response == "Predefined answer."
    assert len(chatbot.get_history()) == 1
    assert chatbot.get_history()[0] == ("What is AI?", "Predefined answer.")

@pytest.mark.asyncio
async def test_get_response_fallback(mock_response_handler):
    async def mock_get_response(*args, **kwargs):
        return "Fallback answer."
    mock_response_handler.get_response.side_effect = mock_get_response
    chatbot = Chatbot(response_handler=mock_response_handler)
    response = await chatbot.get_response("Unknown question?")
    assert response == "Fallback answer."
    assert len(chatbot.get_history()) == 1
    assert chatbot.get_history()[0] == ("Unknown question?", "Fallback answer.")

@pytest.mark.asyncio
async def test_reset_history(mock_response_handler):
    async def mock_get_response(*args, **kwargs):
        return "Answer."
    
    mock_response_handler.get_response.side_effect = mock_get_response
    chatbot = Chatbot(response_handler=mock_response_handler)
    await chatbot.get_response("Hello?")
    chatbot.reset_history()
    assert len(chatbot.get_history()) == 0
