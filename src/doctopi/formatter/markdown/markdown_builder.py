"""TODO"""
# Built-in imports
from __future__ import annotations
from typing import (List, Union)
import os

# Third-party imports

# This package imports
from doctopi.formatter import Command
from doctopi.parser import Parser
from doctopi.parser.parser_factory import ParserFactory

class MarkdownBuilder:  # pylint: disable = too-many-instance-attributes
    """Build a Markdown formatter and generate documentation. Uses the
    builder pattern to handle large amounts of configuration, and the
    command pattern to allow users to customize/organize documentation.

    Attributes:
        src_language (str): Programming language of source code. Should
            be one of "python", "java", "cpp".
        parser (Parser): DoctoPi source code parser.
        src (Union[str, bytes, os.PathLike]): Source file/dir to parse.
        output (Union[str, bytes, os.PathLike]): Markdown output file.
        commands (List[Command]): List of markdon commands to execute
            using the Command pattern. These commands dictate how the
            markdown documentation should be organized.
        recursive (bool): Toggle if the parser should stop at the root
            source directory provided or parse subdirectories. Default
            is False.
        toc_depth (int): Heading depth of the table of contents. Value
            should be [1,6]. Default is 1.
        toc_title (str): Title for the table of contents. Default is
            "Contents".
        table_align (str): Text alignment for all markdown tables. Value
            should be one of "left", "center", or "right. Default is
            "left".
        table_of_contents (bool): Toggle a table of contents to be
            generated. Default is False.
        constructors (bool): Toggle constructors to be documented.
            Default is True.
        class_vars (bool): Toggle class variables to be documented.
            Default is True.
        instance_vars (bool): Toggle instance variables to be
            documented. Default is True.
        inner_classes (bool): Toggle inner classes to be documented.
            Default is True.
        member_functions (bool): Toggle member functions to be
            documented. Default is True.
        file_overview (bool): Toggle file overview to be documented.
            Default is True.
    """
    def __init__(self):
        """Constructor"""
        # Generic
        self.src_language: str = ""  # python, java, or cpp
        self.parser: Parser = None
        self.src: Union[str, bytes, os.PathLike] = None
        self.output: Union[str, bytes, os.PathLike] = None
        self.recursive: bool = False

        # Command pattern
        self.commands: List[Command] = []

        # Table of contents
        self.toc_depth: int = 1 # Should be 1-6
        self.toc_title: str = "Contents"

        # Tables
        self.table_align: str = "left"  # left, center, or right

        # Enabled content
        self.table_of_contents: bool = False
        self.constructors: bool = True
        self.class_vars: bool = True
        self.instance_vars: bool = True
        self.inner_classes: bool = True
        self.member_functions: bool = True
        self.file_overview: bool = True

        #TODO public functions?

    def add_command(self, command: Command) -> MarkdownBuilder:
        """Add a Markdown generation command. Upon calling
        MarkdownBuild.build(), commands will be executed one by one
        to format and generate documentation in markdown.

        Args:
            command (Command): _description_

        Returns:
            MarkdownBuilder: _description_
        """
        self.commands.append(command)
        return self

    def build(self):
        """Generate the markdown by executing the provided commands
        """
        raise NotImplementedError

    def configure_src(self, language: str = "python", style: str = "google") -> MarkdownBuilder:
        """Configure the source progammming language and documentation
        style

        Args:
        language (str, optional): programming language.
            Defaults to "python".
        style (str, optional): source code docstring style/flavor.
            Defaults to "google".

        Returns:
            MarkdownBuilder: This MarkdownBuilder object.
        """
        self.src_language = language
        self.parser = ParserFactory(language=language, style=style)

        return self

    def configure_io(self,
                     src: Union[str, bytes, os.PathLike],
                     output: Union[str, bytes, os.PathLike] = "README.md",
                     recursive: bool = False) -> MarkdownBuilder:
        """Configure the Markdown builder to process a provided source
        file or directory, recursive or not, and set the output markdown
        file path/name.

        Args:
            src (Union[str, bytes, os.PathLike]): Source file/dir to
                parse.
            output (Union[str, bytes, os.PathLike], optional): Markdown
                output file. Defaults to "README.md".
            recursive (bool): Toggle if the parser should stop at the
                root source directory provided or parse subdirectories.
                Defaults to False.

         Raises:
            ValueError: If the src directory/file doesn't exist.

        Returns:
            MarkdownBuilder: This MarkdownBuilder object.
        """
        if not os.path.exists(src):
            raise ValueError(f'"{src}" path does not exist.')

        self.src = src
        self.output = output
        self.recursive = recursive

        return self

    def enable_toc(self, toc_depth: int = 1, title: str = "Contents") -> MarkdownBuilder:
        """Enable a table of contents for the generted markdown.
        Configure the heading depth for the table and the title.

        Args:
            toc_depth (int, optional): Heading depth of the table of
                contents. Value should be [1,6]. Defaults to 1.
            title (str, optional): Title for the table of contents.
                Defaults to "Contents".

        Raises:
            ValueError: If the toc_depth isn't between [1,6]

        Returns:
            MarkdownBuilder: This MarkdownBuilder.
        """
        if not 1 <=  toc_depth <= 6:
            raise ValueError("Table of contents depth must be between 1 & 6.")

        self.table_of_contents = True
        self.toc_depth = toc_depth
        self.toc_title = title

        return self

    def toggle(self, attr: str) -> MarkdownBuilder:
        """Toggle one of the many instance variables. See
        MarkdownBuilder for list of all boolean variables to toggle. By
        default, all are set to True except Table of Contents. To enable
        the Table of contents, use MarkdownBuilder.enable_toc()

        Args:
            attr (str): Instance variable in the MarkdownBuilder class

        Raises:
            ValueError: If the provided attribute does exist but isn't
                a boolean.
            AttributeError: If the provided attribute does not exist.

        Returns:
            MarkdownBuilder: This MarkdownBuilder
        """
        if hasattr(self, attr):
            current_value = getattr(self, attr)
            if isinstance(current_value, bool):
                setattr(self, attr, not current_value)
            else:
                raise ValueError(f"The variable '{attr}' is not a boolean.")
        else:
            raise AttributeError(f"The variable '{attr}' does not exist.")

        return self

    def align_tables(self, alignment: str) -> MarkdownBuilder:
        """Set text inside markdown tables to align left, center, or
        right.

        Args:
            alignment (str): Align text 'left', 'center', or 'right'.

        Raises:
            ValueError: Invalid alignment string provided.

        Returns:
            MarkdownBuilder: This MarkdownBuilder
        """
        if alignment not in ["left", "center", "right"]:
            raise ValueError("alignment must be one of 'left', 'center', or 'right'.")
        self.table_align = alignment
        return self
