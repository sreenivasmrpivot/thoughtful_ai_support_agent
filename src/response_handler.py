# src/response_handler.py

import logging
from typing import List, Optional

import numpy as np

import asyncio.threads
from .config import Config

from langchain_openai import OpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from sklearn.metrics.pairwise import cosine_similarity
import asyncio
from pydantic import SecretStr


logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

class ResponseHandler:
    def __init__(self, questions: List[str], answers: List[str], config: Config):
        if not config.OPENAI_API_KEY:
            logger.error("OPENAI_API_KEY is not set.")
            raise ValueError("OPENAI_API_KEY is not set.")
        
        # Wrap the API key in SecretStr
        openai_api_key = SecretStr(config.OPENAI_API_KEY)
        
        # Pass SecretStr-wrapped API key
        self.questions = questions
        self.answers = answers
        self.config = config
        self.embeddings = OpenAIEmbeddings(api_key=openai_api_key)  # Pass SecretStr here
        self.vector_store = FAISS.from_texts(self.questions, self.embeddings)
        self.llm = OpenAI(api_key=openai_api_key, temperature=0.5)  # Pass SecretStr here
        logger.info("ResponseHandler initialized successfully.")

    async def get_predefined_answer(self, user_query: str) -> Optional[str]:
        try:
            docs = await asyncio.get_event_loop().run_in_executor(
                None, self.vector_store.similarity_search, user_query, 1
            )
            if not docs:
                logger.debug("No documents found in similarity search.")
                return None
            # Compute similarity score
            embedding_query = await asyncio.get_event_loop().run_in_executor(
                None, self.embeddings.embed_query, user_query
            )
            embedding_doc = await asyncio.get_event_loop().run_in_executor(
                None, self.embeddings.embed_query, docs[0].page_content
            )
            
            # Convert lists to numpy arrays
            embedding_query_np = np.array([embedding_query])
            embedding_doc_np = np.array([embedding_doc])
            
            similarity = cosine_similarity(embedding_query_np, embedding_doc_np)[0][0]
            logger.debug(f"Similarity score: {similarity}")
            
            if similarity >= self.config.SIMILARITY_THRESHOLD:
                index = self.questions.index(docs[0].page_content)
                logger.info(f"Predefined answer found for query: '{user_query}'")
                return self.answers[index]
            else:
                logger.info(f"No relevant predefined answer found for query: '{user_query}'")
                return None
        except Exception as e:
            logger.error(f"Error in get_predefined_answer: {e}")
            return None


    async def get_fallback_answer(self, user_query: str) -> str:
        try:
            logger.info(f"Generating fallback answer for query: '{user_query}'")
            response = await asyncio.threads.to_thread(self.llm, user_query)
            return response
        except Exception as e:
            logger.error(f"Error in get_fallback_answer: {e}")
            return "I'm sorry, something went wrong. Please try again later."

    async def get_response(self, user_query: str) -> str:
        predefined = await self.get_predefined_answer(user_query)
        if predefined:
            return predefined
        else:
            return await self.get_fallback_answer(user_query)
