import pytest
from unittest.mock import patch
from shelf_genius.models.shelf_genius_state import ShelfGeniusState
from shelf_genius.nodes.book_recommendation_node import book_recommendation_node


@pytest.fixture
def valid_state():
    return ShelfGeniusState(
        recognized_books=[
            {"title": "Book 1", "author": "Author 1"},
            {"title": "Book 2", "author": "Author 2"},
        ],
        book_metadata=[
            {"title": "Book 1", "authors": ["Author 1"], "categories": ["Category 1"], "description": "Description 1"},
            {"title": "Book 2", "authors": ["Author 2"], "categories": ["Category 2"], "description": "Description 2"},
        ],
    )


@pytest.fixture
def invalid_state_missing_books():
    return ShelfGeniusState(
        recognized_books=[],
        book_metadata=[
            {"title": "Book 1", "authors": ["Author 1"], "categories": ["Category 1"], "description": "Description 1"},
            {"title": "Book 2", "authors": ["Author 2"], "categories": ["Category 2"], "description": "Description 2"},
        ],
    )


@pytest.fixture
def invalid_state_missing_metadata():
    return ShelfGeniusState(
        recognized_books=[
            {"title": "Book 1", "author": "Author 1"},
            {"title": "Book 2", "author": "Author 2"},
        ],
        book_metadata=[],
    )


@patch("shelf_genius.nodes.book_recommendation_node.OpenAI")
def test_book_recommendation_node_valid_state(mock_openai, valid_state):
    mock_openai().chat.completions.create.return_value.choices[0].message.content = """
    {
        "recommendation": {
            "title": "New Book",
            "author": "New Author",
            "reasoning": "Because it matches your interests."
        }
    }
    """
    new_state = book_recommendation_node(valid_state)
    assert "error" not in new_state
    assert "book_recommendation" in new_state
    assert new_state["book_recommendation"]["title"] == "New Book"
    assert new_state["book_recommendation"]["author"] == "New Author"
    assert new_state["book_recommendation"]["reasoning"] == "Because it matches your interests."


@patch("shelf_genius.nodes.book_recommendation_node.OpenAI")
def test_book_recommendation_node_missing_books(mock_openai, invalid_state_missing_books):
    new_state = book_recommendation_node(invalid_state_missing_books)
    assert "error" in new_state
    assert new_state["error"] == "Book recommendation failed: No recognized books found in state"


@patch("shelf_genius.nodes.book_recommendation_node.OpenAI")
def test_book_recommendation_node_missing_metadata(mock_openai, invalid_state_missing_metadata):
    new_state = book_recommendation_node(invalid_state_missing_metadata)
    assert "error" in new_state
    assert new_state["error"] == "Book recommendation failed: No book metadata found in state"
