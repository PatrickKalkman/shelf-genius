from unittest.mock import MagicMock, patch

import pytest

from shelf_genius.models.shelf_genius_state import ShelfGeniusState
from shelf_genius.nodes.book_recognition_node import book_recognition_node


@pytest.fixture
def valid_base64_image():
    return "valid_base64_encoded_image"


@pytest.fixture
def invalid_base64_image():
    return "invalid_base64_encoded_image"


@pytest.fixture
def unrecognizable_books_image():
    return "unrecognizable_books_base64_encoded_image"


def mock_pipe(self, other):
    return other


@patch("langchain.prompts.prompt.PromptTemplate.__or__", new=mock_pipe)
@patch("langchain_openai.OpenAI")
def test_book_recognition_with_valid_image(mock_openai, valid_base64_image):
    # Set up mock chain response
    mock_llm = MagicMock()
    mock_llm.invoke.return_value = [
        {"title": "Book Title 1", "author": "Author 1"},
        {"title": "Book Title 2", "author": "Author 2"},
    ]
    mock_openai.return_value = mock_llm

    # Create initial state and run node
    state = ShelfGeniusState(image_base64=valid_base64_image)
    new_state = book_recognition_node(state)

    # Verify results
    assert "error" not in new_state
    assert len(new_state["recognized_books"]) == 2
    assert new_state["recognized_books"][0]["title"] == "Book Title 1"
    assert new_state["recognized_books"][0]["author"] == "Author 1"
    assert new_state["recognized_books"][1]["title"] == "Book Title 2"
    assert new_state["recognized_books"][1]["author"] == "Author 2"


@patch("langchain.prompts.prompt.PromptTemplate.__or__", mock_pipe)
@patch("langchain_openai.OpenAI")
def test_book_recognition_with_invalid_image(mock_openai, invalid_base64_image):
    # Set up mock chain to raise exception
    mock_llm = MagicMock()
    mock_llm.invoke.side_effect = Exception("Invalid image format")
    mock_openai.return_value = mock_llm

    # Create initial state and run node
    state = ShelfGeniusState(image_base64=invalid_base64_image)
    new_state = book_recognition_node(state)

    # Verify error handling
    assert "error" in new_state
    assert new_state["error"] == "Book recognizing failed: Invalid image format"


@patch("langchain.prompts.prompt.PromptTemplate.__or__", mock_pipe)
@patch("langchain_openai.OpenAI")
def test_book_recognition_with_unrecognizable_books(mock_openai, unrecognizable_books_image):
    # Set up mock chain response with some unrecognizable books
    mock_llm = MagicMock()
    mock_llm.invoke.return_value = [
        {"title": "", "author": ""},
        {"title": "Book Title 1", "author": "Author 1"},
        {"title": "", "author": ""},
    ]
    mock_openai.return_value = mock_llm

    # Create initial state and run node
    state = ShelfGeniusState(image_base64=unrecognizable_books_image)
    new_state = book_recognition_node(state)

    # Verify filtering of unrecognizable books
    assert "error" not in new_state
    assert len(new_state["recognized_books"]) == 1
    assert new_state["recognized_books"][0]["title"] == "Book Title 1"
    assert new_state["recognized_books"][0]["author"] == "Author 1"
