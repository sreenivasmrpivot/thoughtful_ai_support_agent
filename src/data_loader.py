# src/data_loader.py

import json
import os
import logging
from typing import List

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

class DataLoader:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.questions: List[str] = []
        self.answers: List[str] = []
        self.load_data()

    def load_data(self):
        if not os.path.exists(self.filepath):
            logger.error(f"Predefined data file not found at {self.filepath}")
            raise FileNotFoundError(f"Predefined data file not found at {self.filepath}")
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.questions = [item["question"] for item in data["questions"]]
                self.answers = [item["answer"] for item in data["questions"]]
                logger.info(f"Loaded {len(self.questions)} predefined Q&A pairs.")
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON: {e}")
            raise e

    def get_questions(self) -> List[str]:
        return self.questions

    def get_answers(self) -> List[str]:
        return self.answers
