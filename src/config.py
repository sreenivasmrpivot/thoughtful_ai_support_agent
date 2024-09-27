# src/config.py

import os
from dataclasses import dataclass
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

@dataclass
class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    SIMILARITY_THRESHOLD: float = 0.75
    PORT: int = int(os.getenv("PORT", 7860))
    HOST: str = os.getenv("HOST", "0.0.0.0")
