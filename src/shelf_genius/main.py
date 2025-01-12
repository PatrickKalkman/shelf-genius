import asyncio
from typing import Any, Dict

from dotenv import load_dotenv
from langgraph.graph import END, StateGraph
from loguru import logger

from shelf_genius.models.shelf_genius_state import ShelfGeniusState
from shelf_genius.nodes.book_lookup_node import book_lookup_node
from shelf_genius.nodes.book_recognition_node import book_recognition_node
from shelf_genius.nodes.book_recommendation_node import book_recommendation_node
from shelf_genius.nodes.process_image_node import process_image_node


def create_workflow(config: Dict[str, Any]) -> StateGraph:
    workflow = StateGraph(ShelfGeniusState)

    workflow.add_node("process_image_node", process_image_node)
    workflow.add_node("book_recognition_node", book_recognition_node)
    workflow.add_node("book_lookup_node", book_lookup_node)
    workflow.add_node("book_recommendation_node", book_recommendation_node)

    workflow.set_entry_point("process_image_node")

    workflow.add_edge("process_image_node", "book_recognition_node")
    workflow.add_edge("book_recognition_node", "book_lookup_node")
    workflow.add_edge("book_lookup_node", "book_recommendation_node")
    workflow.add_edge("book_recommendation_node", END)

    return workflow.compile()


async def run_workflow_async(config: Dict[str, Any]) -> ShelfGeniusState:
    """Run the GitSage workflow asynchronously and return the final state."""
    initial_state: ShelfGeniusState = {
        "errors": [],
        "warnings": [],
    }

    app = create_workflow(config)
    final_state = None
    async for state in app.astream(initial_state):
        final_state = list(state.values())[0]
        if "errors" in final_state and final_state["errors"]:
            logger.error("Errors encountered:", final_state["errors"])

    return final_state


def run_workflow(config: Dict[str, Any]) -> ShelfGeniusState:
    """Synchronous wrapper for the async workflow."""
    return asyncio.run(run_workflow_async(config))


def main():
    load_dotenv()

    logger.info("Starting Shelf Genius workflow...")
    config = {
        "image_path": "path/to/image.jpg",
    }
    final_state = run_workflow(config)
    logger.info("Shelf Genius workflow completed.")
    logger.info("Final state:", final_state)


if __name__ == "__main__":
    main()
