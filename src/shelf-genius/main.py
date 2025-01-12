from typing import Dict, Any

from loguru import logger

from .models.shelf_genius_state import ShelfGeniusState
from .nodes.process_image_node import process_image_node
from .workflow import StateGraph, END


def create_workflow(config: Dict[str, Any]) -> StateGraph:
    """
    Create the Shelf Genius workflow graph.
    
    Args:
        config: Configuration dictionary for the workflow
        
    Returns:
        Compiled workflow graph
    """
    workflow = StateGraph(ShelfGeniusState)

    # Add nodes
    workflow.add_node("process_image", process_image_node)
    
    # Set entry point
    workflow.set_entry_point("process_image")
    
    # Define edges
    workflow.add_edge("process_image", END)

    return workflow.compile()


def run_workflow(config: Dict[str, Any]) -> ShelfGeniusState:
    """
    Execute the Shelf Genius workflow.
    
    Args:
        config: Configuration dictionary for the workflow
        
    Returns:
        Final state after workflow execution
    """
    try:
        # Initialize workflow
        workflow = create_workflow(config)
        
        # Initialize state
        state = ShelfGeniusState(
            conversation_history=[],
            current_step="initializing",
            error=None
        )
        
        # Execute workflow
        current_node = workflow.entry_point
        while current_node != "END":
            logger.info(f"Executing node: {current_node}")
            
            # Execute current node
            node_fn = workflow.nodes[current_node]
            state = node_fn(state)
            
            # Check for errors
            if state.get("error"):
                logger.error(f"Workflow failed at {current_node}: {state['error']}")
                return state
                
            # Move to next node
            current_node = workflow.edges[current_node]
            
        logger.info("Workflow completed successfully")
        return state
        
    except Exception as e:
        error_msg = f"Unexpected error in workflow: {str(e)}"
        logger.error(error_msg)
        state = ShelfGeniusState(
            conversation_history=[],
            current_step="error",
            error=error_msg
        )
        return state
