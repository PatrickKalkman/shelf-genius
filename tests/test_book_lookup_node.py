import pytest
import requests
from unittest.mock import patch

from shelf_genius.nodes.book_lookup_node import get_book_metadata_from_openlibrary, book_lookup_node
from shelf_genius.models.shelf_genius_state import ShelfGeniusState, BookInfo


def test_get_book_metadata_from_openlibrary():
    title = "The Great Gatsby"
    author = "F. Scott Fitzgerald"
    expected_metadata = {
        "title": "The Great Gatsby",
        "author_name": ["F. Scott Fitzgerald"],
        "first_publish_year": 1925,
    }

    with patch("requests.get") as mock_get:
        mock_response = mock_get.return_value
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"docs": [expected_metadata]}

        metadata = get_book_metadata_from_openlibrary(title, author)
        assert metadata == expected_metadata


def test_book_lookup_node():
    state = ShelfGeniusState(
        recognized_books=[
            BookInfo(title="The Great Gatsby", author="F. Scott Fitzgerald"),
            BookInfo(title="1984", author="George Orwell"),
        ]
    )

    google_metadata = {
        "title": "The Great Gatsby",
        "authors": ["F. Scott Fitzgerald"],
        "publishedDate": "1925",
    }

    openlibrary_metadata = {
        "title": "The Great Gatsby",
        "author_name": ["F. Scott Fitzgerald"],
        "first_publish_year": 1925,
    }

    with patch("shelf_genius.nodes.book_lookup_node.get_book_metadata") as mock_google, \
         patch("shelf_genius.nodes.book_lookup_node.get_book_metadata_from_openlibrary") as mock_openlibrary:
        mock_google.return_value = google_metadata
        mock_openlibrary.return_value = openlibrary_metadata

        new_state = book_lookup_node(state)

        assert "error" not in new_state
        assert len(new_state["book_metadata"]) == 2
        assert new_state["book_metadata"][0]["title"] == "The Great Gatsby"
        assert new_state["book_metadata"][0]["authors"] == ["F. Scott Fitzgerald"]
        assert new_state["book_metadata"][0]["first_publish_year"] == 1925
        assert new_state["book_metadata"][1]["title"] == "1984"
