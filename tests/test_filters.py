"""Tests for GIMP MCP filters pack."""
from gimp_mcp.filters import sharpen, emboss, brightness_contrast


def test_sharpen_callable():
    assert callable(sharpen)


def test_emboss_callable():
    assert callable(emboss)


def test_brightness_contrast_callable():
    assert callable(brightness_contrast)
