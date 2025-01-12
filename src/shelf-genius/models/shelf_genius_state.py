from typing import TypedDict, Optional, List, Dict, Any


class ShelfGeniusState(TypedDict, total=False):
    """State management for the Shelf Genius agent."""

    # Placeholder for state fields - to be expanded later
    conversation_history: List[Dict[str, Any]]
    current_step: str
    error: Optional[str]
