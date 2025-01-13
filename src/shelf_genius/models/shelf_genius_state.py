from typing import Any, Dict, List, Optional, TypedDict


class ShelfGeniusState(TypedDict, total=False):
    """State management for the Shelf Genius agent."""

    image_path: str
    image_width: int
    image_height: int
    image_format: str
    image_original_path: str
    image_base64: str
    # Placeholder for state fields - to be expanded later
    conversation_history: List[Dict[str, Any]]
    current_step: str
    error: Optional[str]

    errors: List[Dict[str, Any]]
    warnings: List[Dict[str, Any]]
