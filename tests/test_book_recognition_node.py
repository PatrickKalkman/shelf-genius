from unittest.mock import patch

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


@patch("shelf_genius.nodes.book_recognition_node.LLMChain.run")
def test_book_recognition_with_valid_image(mock_run, valid_base64_image):
    mock_run.return_value = [
        {"title": "Book Title 1", "author": "Author 1"},
        {"title": "Book Title 2", "author": "Author 2"},
    ]
    state = ShelfGeniusState(image_base64=valid_base64_image)
    new_state = book_recognition_node(state)
    assert "error" not in new_state
    assert len(new_state["recognized_books"]) == 2
    assert new_state["recognized_books"][0]["title"] == "Book Title 1"
    assert new_state["recognized_books"][0]["author"] == "Author 1"
    assert new_state["recognized_books"][1]["title"] == "Book Title 2"
    assert new_state["recognized_books"][1]["author"] == "Author 2"


@patch("shelf_genius.nodes.book_recognition_node.LLMChain.run")
def test_book_recognition_with_invalid_image(mock_run, invalid_base64_image):
    mock_run.side_effect = Exception("Invalid image format")
    state = ShelfGeniusState(image_base64=invalid_base64_image)
    new_state = book_recognition_node(state)
    assert "error" in new_state
    assert new_state["error"] == "Book recognizing failed: Invalid image format"


@patch("shelf_genius.nodes.book_recognition_node.LLMChain.run")
def test_book_recognition_with_unrecognizable_books(mock_run, unrecognizable_books_image):
    mock_run.return_value = [
        {"title": "", "author": ""},
        {"title": "Book Title 1", "author": "Author 1"},
        {"title": "", "author": ""},
    ]
    state = ShelfGeniusState(image_base64=unrecognizable_books_image)
    new_state = book_recognition_node(state)
    assert "error" not in new_state
    assert len(new_state["recognized_books"]) == 1
    assert new_state["recognized_books"][0]["title"] == "Book Title 1"
    assert new_state["recognized_books"][0]["author"] == "Author 1"
