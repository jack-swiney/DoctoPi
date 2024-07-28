"""The Doctopi MarkdownBuilder class uses the Command design pattern to
let the user customize the documentation for various types. The
MarkdownFunctionCommand is used to define how to document a function.
"""
# pylint: disable = too-few-public-methods

# Built-in imports
from __future__ import annotations
from typing import (List, Type)

# Third-party imports
from mdutils.mdutils import MdUtils

# This package imports
from doctopi.types import (AccessType, Command, FunctionDeclaration, MarkdownSettings)
from doctopi.formatter.markdown.cmd.docstring_commands import (MarkdownDocstringCommand)


class MarkdownFunctionCommand(Command):
    """The MarkdownFunctionCommand is used to define how to document a
    function. It uses various sub-commands to document params, returns,
    exceptions, etc.

    Attributes:
        md_utils (MdUtils): Markdown file generator
        settings (MarkdownSettings): Markdown generator settings
        level (int): Heading level to write the Class in markdown
        func (FunctionDelcaration): The function to document
        cmds (List[MarkdownDocstringCommand]): List of commands
            to execute in order to document params, returns, and
            exceptions
    """
    # pylint: disable = too-many-arguments
    def __init__(self,
                 md_utils: MdUtils,
                 settings: MarkdownSettings,
                 level: int,
                 func: FunctionDeclaration,
                 cmds: List[Type[MarkdownDocstringCommand]]):
        if not 1 <= level:
            raise ValueError("Level must be between [1,6]")

        self.md_utils = md_utils
        self.settings = settings
        self.level = min(level, 6)  # Can't go any higher than 6, so flatten at 6.
        self.func = func
        self.commands = cmds

    def execute(self):
        """Add function documentation to the markdown generator"""
        # Ignore if the function isn't public and public_only is set
        if self.settings.public_only and self.func.access != AccessType.PUBLIC:
            return

        # Header with function signature
        self.md_utils.new_header(level=self.level, title=self.func.name)
        self.md_utils.insert_code(
            self.func.signature,
            language=self.settings.src_language
        )
        # Include the summary/description
        if self.func.docstring:
            self.md_utils.new_paragraph(self.func.docstring.summary)

            # Document the params/exceptions/return type via command pattern
            for cmd in self.commands:
                cmd(md_utils=self.md_utils,
                    settings=self.settings,
                    level=self.level+1,
                    docstring=self.func.docstring).execute()
