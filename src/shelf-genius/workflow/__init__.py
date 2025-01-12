from typing import TypeVar, Callable, Dict, Any
from dataclasses import dataclass
from enum import Enum

from ..models.shelf_genius_state import ShelfGeniusState

# Type for state
StateType = TypeVar("StateType", bound=ShelfGeniusState)

# Type for node functions
NodeFn = Callable[[StateType], StateType]

class END(Enum):
    """Sentinel value indicating end of workflow"""
    token = 1

@dataclass
class StateGraph:
    """Graph representation of a workflow"""
    state_type: type[StateType]
    nodes: Dict[str, NodeFn]
    edges: Dict[str, str]
    entry_point: str

    def __init__(self, state_type: type[StateType]):
        self.state_type = state_type
        self.nodes = {}
        self.edges = {}
        self.entry_point = ""

    def add_node(self, name: str, fn: NodeFn) -> None:
        """Add a node to the workflow"""
        self.nodes[name] = fn

    def add_edge(self, from_node: str, to_node: str | END) -> None:
        """Add an edge between nodes"""
        if isinstance(to_node, END):
            self.edges[from_node] = "END"
        else:
            self.edges[from_node] = to_node

    def set_entry_point(self, node: str) -> None:
        """Set the entry point node"""
        if node not in self.nodes:
            raise ValueError(f"Entry point {node} not found in nodes")
        self.entry_point = node

    def compile(self) -> 'StateGraph':
        """Validate and return the workflow"""
        if not self.entry_point:
            raise ValueError("No entry point set")
        if not self.nodes:
            raise ValueError("No nodes added to workflow")
        return self
