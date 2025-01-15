import base64
import io
from typing import TypeVar

from loguru import logger
from PIL import Image, ImageOps

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


def resize_image(img: Image.Image, max_dimension: int = 1024) -> Image.Image:
    """Resize image maintaining aspect ratio if it exceeds max dimension"""
    width, height = img.size
    if width > max_dimension or height > max_dimension:
        scale = max_dimension / max(width, height)
        new_size = (int(width * scale), int(height * scale))
        return img.resize(new_size, Image.Resampling.LANCZOS)
    return img


def optimize_image_for_recognition(img: Image.Image) -> Image.Image:
    """Apply optimizations to improve text recognition"""
    # Convert to grayscale
    img = ImageOps.grayscale(img)

    # Enhance contrast
    img = ImageOps.autocontrast(img, cutoff=0.5)

    # Optionally sharpen the image
    # from PIL import ImageEnhance
    # enhancer = ImageEnhance.Sharpness(img)
    # img = enhancer.enhance(1.5)

    return img


def process_image_node(state: AgentState) -> AgentState:
    try:
        logger.info("Processing bookshelf image...")

        image_path = state.get("image_path")
        if not image_path:
            raise ValueError("Image path is missing in the state.")

        if not validate_image_format(image_path):
            raise ValueError("Unsupported image format. Only jpg and png are supported.")

        with Image.open(image_path) as img:
            # Store original image metadata
            state["image_original_width"] = img.width
            state["image_original_height"] = img.height
            state["image_format"] = img.format
            state["image_original_path"] = image_path

            # Resize image if necessary
            img = resize_image(img, max_dimension=512)

            # Optimize image for text recognition
            img = optimize_image_for_recognition(img)

            # Store processed image metadata
            state["image_width"] = img.width
            state["image_height"] = img.height

            # Convert processed image to base64
            buffered = io.BytesIO()
            img.save(buffered, format="JPEG", quality=85, optimize=True)
            img_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
            state["image_base64"] = img_base64

            # Log processing results
            reduction = (1 - (len(img_base64) / (img.width * img.height))) * 100
            logger.info(
                f"Image {image_path} processed successfully. "
                f"Original size: ({state['image_original_width']}, {state['image_original_height']}), "
                f"New size: ({img.width}, {img.height}), "
                f"Approximate reduction: {reduction:.1f}%"
            )

        state["current_step"] = "process_image_node"
        return state

    except Exception as e:
        logger.error(f"Error processing image: {str(e)}")
        state["error"] = f"Image processing failed: {str(e)}"
        return state
