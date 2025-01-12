from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class ShelfGeniusState(BaseModel):
    """State management for the Shelf Genius agent."""
    
    # Placeholder for state fields - to be expanded later
    conversation_history: List[Dict[str, Any]] = Field(default_factory=list)
    current_step: str = Field(default="initialize")
    error: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True
