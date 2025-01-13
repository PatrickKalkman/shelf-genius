import requests
from loguru import logger

from shelf_genius.models.shelf_genius_state import ShelfGeniusState


def get_book_metadata(title: str, author: str) -> dict:
    """Retrieve book metadata from Google Books API."""
    try:
        query = f"intitle:{title}+inauthor:{author}"
        response = requests.get(
            "https://www.googleapis.com/books/v1/volumes",
            params={"q": query},
        )
        response.raise_for_status()
        items = response.json().get("items", [])
        if items:
            return items[0].get("volumeInfo", {})
        return {}
    except Exception as e:
        logger.error(f"Error fetching book metadata: {str(e)}")
        return {}
    try:
        # TODO: Implement actual book lookup logic
        # This is a placeholder that will be expanded with actual book lookup
        logger.info("Starting book look up node...")

        # Retrieve metadata for each recognized book
        book_metadata = []
        for book in state.get("recognized_books", []):
            metadata = get_book_metadata(book["title"], book["author"])
            if metadata:
                book_metadata.append(metadata)

        # Update state with processed information
        state["book_metadata"] = book_metadata
        state["current_step"] = "book_lookup_node"

        return state

    except Exception as e:
        logger.error(f"Error while looking up books: {str(e)}")
        state["error"] = f"Book lookup failed: {str(e)}"
        return state
