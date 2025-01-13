from typing import TypeVar

from loguru import logger
from PIL import Image

from shelf_genius.models.shelf_genius_state import ShelfGeniusState

AgentState = TypeVar("AgentState", bound=ShelfGeniusState)


def validate_image_format(image_path: str) -> bool:
    valid_formats = ["JPEG", "PNG"]
    try:
        with Image.open(image_path) as img:
            if img.format not in valid_formats:
                return False
    except Exception as e:
        logger.error(f"Error validating image format: {str(e)}")
        return False
    return True


def process_image_node(state: AgentState) -> AgentState:
    try:
        logger.info("Processing bookshelf image...")

        image_path = state.get("image_path")
        if not image_path:
            raise ValueError("Image path is missing in the state.")

        if not validate_image_format(image_path):
            raise ValueError("Unsupported image format. Only jpg and png are supported.")

        with Image.open(image_path) as img:
            # Placeholder for actual image processing logic
            logger.info(f"Image {image_path} loaded successfully. {img.size}")

        state["current_step"] = "process_image_node"

        return state

    except Exception as e:
        logger.error(f"Error processing image: {str(e)}")
        state["error"] = f"Image processing failed: {str(e)}"
        return state
