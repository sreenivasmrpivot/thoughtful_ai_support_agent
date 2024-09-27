# tests/test_response_handler.py

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from src.response_handler import ResponseHandler
from src.config import Config

@pytest.fixture
def config():
    cfg = Config()
    cfg.OPENAI_API_KEY = "test_key"
    cfg.SIMILARITY_THRESHOLD = 0.75
    return cfg

@pytest.fixture
def questions_answers():
    questions = ["What is AI?"]
    answers = ["AI stands for Artificial Intelligence."]
    return questions, answers

@patch('src.response_handler.OpenAIEmbeddings')
@patch('src.response_handler.FAISS')
@patch('src.response_handler.OpenAI')
@pytest.mark.asyncio
async def test_get_predefined_answer_found(mock_llm, mock_faiss, mock_embeddings, config, questions_answers):
    questions, answers = questions_answers
    mock_faiss_instance = mock_faiss.from_texts.return_value
    mock_faiss_instance.similarity_search.return_value = [MagicMock(page_content="What is AI?")]
    mock_embeddings_instance = mock_embeddings.return_value
    mock_embeddings_instance.embed_query.return_value = [1, 0, 0]
    
    handler = ResponseHandler(questions, answers, config)
    answer = await handler.get_predefined_answer("Define AI")
    assert answer == "AI stands for Artificial Intelligence."

@patch('src.response_handler.OpenAIEmbeddings')
@patch('src.response_handler.FAISS')
@patch('src.response_handler.OpenAI')
@pytest.mark.asyncio
async def test_get_predefined_answer_not_found(mock_llm, mock_faiss, mock_embeddings, config, questions_answers):
    questions, answers = questions_answers
    mock_faiss_instance = mock_faiss.from_texts.return_value
    mock_faiss_instance.similarity_search.return_value = [MagicMock(page_content="What is AI?")]
    mock_embeddings_instance = mock_embeddings.return_value
    mock_embeddings_instance.embed_query.side_effect = [
        [1, 0, 0],  # user_query embedding
        [0, 1, 0]   # document embedding
    ]
    
    handler = ResponseHandler(questions, answers, config)
    answer = await handler.get_predefined_answer("Tell me about machine learning")
    assert answer is None

@patch('src.response_handler.OpenAI')
@pytest.mark.asyncio
async def test_get_fallback_answer(mock_llm, config):
    # Use AsyncMock for asynchronous __call__
    mock_llm_instance = mock_llm.return_value
    mock_llm_instance.__call__ = AsyncMock(return_value="This is a fallback answer.")
    
    handler = ResponseHandler(["Q1"], ["A1"], config)
    answer = await handler.get_fallback_answer("Unknown question")
    assert answer == "This is a fallback answer."

@patch('src.response_handler.OpenAIEmbeddings')
@patch('src.response_handler.FAISS')
@patch('src.response_handler.OpenAI')
@pytest.mark.asyncio
async def test_get_response_predefined(mock_llm, mock_faiss, mock_embeddings, config, questions_answers):
    questions, answers = questions_answers
    mock_faiss_instance = mock_faiss.from_texts.return_value
    mock_faiss_instance.similarity_search.return_value = [MagicMock(page_content="What is AI?")]
    mock_embeddings_instance = mock_embeddings.return_value
    mock_embeddings_instance.embed_query.side_effect = [
        [1, 0, 0],  # user_query embedding
        [1, 0, 0]   # document embedding
    ]
    
    handler = ResponseHandler(questions, answers, config)
    response = await handler.get_response("Define AI")
    assert response == "AI stands for Artificial Intelligence."

@patch('src.response_handler.OpenAIEmbeddings')
@patch('src.response_handler.FAISS')
@patch('src.response_handler.OpenAI')
@pytest.mark.asyncio
async def test_get_response_fallback(mock_llm, mock_faiss, mock_embeddings, config, questions_answers):
    questions, answers = questions_answers
    
    # Mock FAISS's behavior
    mock_faiss_instance = mock_faiss.from_texts.return_value
    mock_faiss_instance.similarity_search.return_value = []

    # Mock OpenAI's __call__ method as an async method
    mock_llm_instance = mock_llm.return_value
    mock_llm_instance.__call__ = AsyncMock(return_value="Fallback response")
    
    # Create the ResponseHandler and test the fallback response
    handler = ResponseHandler(questions, answers, config)
    response = await handler.get_response("Unknown question")
    
    assert response == "Fallback response."
