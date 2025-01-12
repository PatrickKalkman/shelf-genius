"""
Basic test suite for ShelfGenius.
"""

from importlib import metadata


def test_version():
    """
    Verify that the package version is properly set and accessible.
    This test ensures our build configuration is working correctly.
    """
    version = metadata.version("shelf-genius")
    assert version == "0.1.0"
