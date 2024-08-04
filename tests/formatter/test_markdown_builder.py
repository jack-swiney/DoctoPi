"""Test the doctopi.formatter.markdown.markdown_builder package"""
# Built-in imports
import os

# Third-party imports
import pytest

# This package imports
from doctopi.formatter.markdown.markdown_builder import MarkdownBuilder
from doctopi.formatter.markdown.cmd import *

class TestMarkdownBuilder:
    """Test the doctopi.formatter.markdown.markdown_builder package"""

    def test_config_functions(self):
        """Test the configuration functions work using the builder
        pattern"""

        # Run through all the builder commands
        builder = MarkdownBuilder() \
            .add_file_command(MarkdownClassCommand) \
            .add_class_commands(MarkdownClassVarCommand) \
            .add_function_commands(MarkdownArgsCommand) \
            .configure_metadata("My Title", "Mr. J Author") \
            .configure_src(language="python", style="auto") \
                .configure_io(os.path.join(os.path.dirname(__file__), "../examples"),
                              "README.md", recursive=True) \
            .enable_toc(4, "My Table of Contents") \
            .toggle("inner_classes") \
            .align_tables("right")

        # Verify align_tables fails if the alignment isn't left/center/right
        with pytest.raises(ValueError):
            builder.align_tables("up")

        # Verify toggling an attribute that doesn't exist fails
        with pytest.raises(AttributeError):
            builder.toggle("some_fake_attr")

        # Verify toggling an attribute that isn't a bool fails
        with pytest.raises(ValueError):
            builder.toggle("src")

        # Verify TOC depth fails if not in [1,6]
        with pytest.raises(ValueError):
            builder.enable_toc(7, "My Table of Contents")
        with pytest.raises(ValueError):
            builder.enable_toc(0, "My Table of Contents")

        # Verify configuring the IO fails is the path is fake
        with pytest.raises(ValueError):
            builder.configure_io("some/fake/path", "README.md", recursive=True)
