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


def book_lookup_node(state: ShelfGeniusState) -> ShelfGeniusState:
    """Retrieve book metadata from Google Books API."""
    try:
        logger.info("Starting book look up node...")
        recognized_books = state.get("recognized_books", [])
        logger.info(f"Found {len(recognized_books)} recognized books in state")
        logger.info(f"Recognized books: {recognized_books}")
        book_metadata = []
        for book in state.get("recognized_books", []):
            title = book.title
            author = book.author
            logger.info(f"Looking up book: {title} by {author}")
            metadata = get_book_metadata(title, author)
            if metadata:
                logger.info(f"Found metadata for {title} by {author}")
                book_metadata.append(metadata)

        # Update state with processed information
        state["book_metadata"] = book_metadata
        state["current_step"] = "book_lookup_node"

        return state

    except Exception as e:
        logger.error(f"Error while looking up books: {str(e)}")
        state["error"] = f"Book lookup failed: {str(e)}"
        return state
