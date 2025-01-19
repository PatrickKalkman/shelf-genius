import pytest
from PIL import Image

from shelf_genius.models.shelf_genius_state import ShelfGeniusState
from shelf_genius.nodes.process_image_node import process_image_node


@pytest.fixture
def valid_jpg_image(tmp_path):
    img_path = tmp_path / "test.jpg"
    img = Image.new("RGB", (100, 100), color="red")
    img.save(img_path)
    return img_path


@pytest.fixture
def valid_png_image(tmp_path):
    img_path = tmp_path / "test.png"
    img = Image.new("RGB", (100, 100), color="blue")
    img.save(img_path)
    return img_path


@pytest.fixture
def invalid_image(tmp_path):
    img_path = tmp_path / "test.bmp"
    img = Image.new("RGB", (100, 100), color="green")
    img.save(img_path)
    return img_path


def test_process_valid_jpg_image(valid_jpg_image):
    state = ShelfGeniusState(image_path=str(valid_jpg_image))
    new_state = process_image_node(state)
    assert "error" not in new_state
    assert new_state["image_width"] == 100
    assert new_state["image_height"] == 100
    assert new_state["image_format"] == "JPEG"
    assert new_state["image_original_path"] == str(valid_jpg_image)
    assert "image_base64" in new_state


def test_process_valid_png_image(valid_png_image):
    state = ShelfGeniusState(image_path=str(valid_png_image))
    new_state = process_image_node(state)
    assert "error" not in new_state
    assert new_state["image_width"] == 100
    assert new_state["image_height"] == 100
    assert new_state["image_format"] == "PNG"
    assert new_state["image_original_path"] == str(valid_png_image)
    assert "image_base64" in new_state


def test_process_invalid_image(invalid_image):
    state = ShelfGeniusState(image_path=str(invalid_image))
    new_state = process_image_node(state)
    assert "error" in new_state
    assert new_state["error"] == "Image processing failed: Unsupported image format. Only jpg and png are supported."


def test_process_image_node(valid_jpg_image):
    state = ShelfGeniusState(image_path=str(valid_jpg_image))
    new_state = process_image_node(state)
    assert "error" not in new_state
    assert new_state["image_width"] == 100
    assert new_state["image_height"] == 100
    assert new_state["image_format"] == "JPEG"
    assert new_state["image_original_path"] == str(valid_jpg_image)
    assert "image_base64" in new_state


def test_process_image_node_invalid_image(invalid_image):
    state = ShelfGeniusState(image_path=str(invalid_image))
    new_state = process_image_node(state)
    assert "error" in new_state
    assert new_state["error"] == "Image processing failed: Unsupported image format. Only jpg and png are supported."
