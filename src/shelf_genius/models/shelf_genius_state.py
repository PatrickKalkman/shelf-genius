from dataclasses import dataclass
from typing import Any, Dict, List, Optional, TypedDict


@dataclass
class BookInfo:
    title: str
    author: str


class ShelfGeniusState(TypedDict, total=False):
    """State management for the Shelf Genius agent."""

    image_path: str
    image_width: int
    image_height: int
    image_format: str
    image_original_path: str
    image_base64: str
    recognized_books: List[BookInfo]
    book_metadata: List[Dict[str, Any]]

    current_step: str
    error: Optional[str]

    errors: List[Dict[str, Any]]
    warnings: List[Dict[str, Any]]
