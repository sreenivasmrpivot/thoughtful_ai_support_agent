# tests/test_data_loader.py

import pytest
from src.data_loader import DataLoader
import os
import json

@pytest.fixture
def sample_data(tmp_path):
    data = {
        "questions": [
            {
                "question": "Test question?",
                "answer": "Test answer."
            }
        ]
    }
    file = tmp_path / "test_predefined_data.json"
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(data, f)
    return file

def test_load_data_success(sample_data):
    loader = DataLoader(filepath=str(sample_data))
    assert loader.get_questions() == ["Test question?"]
    assert loader.get_answers() == ["Test answer."]

def test_load_data_file_not_found():
    with pytest.raises(FileNotFoundError):
        DataLoader(filepath='non_existent_file.json')

def test_load_data_invalid_json(tmp_path):
    file = tmp_path / "invalid.json"
    with open(file, 'w', encoding='utf-8') as f:
        f.write("Invalid JSON")
    with pytest.raises(json.JSONDecodeError):
        DataLoader(filepath=str(file))
