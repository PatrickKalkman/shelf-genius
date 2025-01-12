from typing import Any, Dict, List, Optional, TypedDict


class ShelfGeniusState(TypedDict, total=False):
    """State management for the Shelf Genius agent."""

    image_path: str
    # Placeholder for state fields - to be expanded later
    conversation_history: List[Dict[str, Any]]
    current_step: str
    error: Optional[str]

    errors: List[Dict[str, Any]]
    warnings: List[Dict[str, Any]]
