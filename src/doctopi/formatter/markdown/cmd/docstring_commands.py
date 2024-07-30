"""The Doctopi MarkdownBuilder class uses the Command design pattern to
let the user customize the documentation for various types. The
MarkdownDocstringCommand is used to define how to document the params,
exceptions, and returns of a function.
"""
# pylint: disable = too-few-public-methods

# Third-party imports
from mdutils.mdutils import MdUtils

# This package imports
from doctopi.types import Command, Docstring, MarkdownSettings
from doctopi.formatter.markdown.cmd.param_table_command import MarkdownParamTableCommand


class MarkdownDocstringCommand(Command):
    """Generic class for markdown commands specific to docstring params

    Attributes:
        md_utils (MdUtils): Markdown file generator
        settings (MarkdownSettings): Markdown generator settings
        level (int): Heading level to write the Class in markdown
        docstring (Docstring]): docstring to document
    """
    def __init__(self,
                 md_utils: MdUtils,
                 settings: MarkdownSettings,
                 level: int,
                 docstring: Docstring):
        if not 1 <= level:
            raise ValueError("Level must be between [1,6]")

        self.md_utils = md_utils
        self.settings = settings
        self.level = min(level, 6)  # Can't go any higher than 6, so flatten at 6.
        self.docstring = docstring


class MarkdownArgsCommand(MarkdownDocstringCommand):
    """The MarkdownArgsCommand is used to define how to document
    function arguments from a docstring into markdown.

    Attributes:
        md_utils (MdUtils): Markdown file generator
        level (int): Heading level to write the Class in markdown
        params (List[NameDescriptionType]): Table contents
    """
    def execute(self):
        """Add function argument documentation to the markdown generator"""
        if self.docstring.args:
            self.md_utils.new_header(level=self.level, title="Args")
            MarkdownParamTableCommand(self.md_utils, self.settings, self.docstring.args).execute()


class MarkdownRaisesCommand(MarkdownDocstringCommand):
    """The MarkdownRaisesCommand is used to define how to document
    exceptions a function raises from a docstring into markdown.

    Attributes:
        md_utils (MdUtils): Markdown file generator
        level (int): Heading level to write the Class in markdown
        params (List[NameDescriptionType]): Table contents
    """
    def execute(self):
        """Add function exception documentation to the markdown
        generator
        """
        if self.docstring.raises:
            self.md_utils.new_header(level=self.level, title="Raises")
            MarkdownParamTableCommand(self.md_utils, self.settings, self.docstring.raises).execute()


class MarkdownReturnsCommand(MarkdownDocstringCommand):
    """The MarkdownReturnsCommand is used to define how to document
    a function's return type from a docstring into markdown.

    Attributes:
        md_utils (MdUtils): Markdown file generator
        level (int): Heading level to write the Class in markdown
        params (List[NameDescriptionType]): Table contents
    """
    def execute(self):
        """Add function returns documentation to the markdown generator"""
        if not self.docstring.returns:
            return

        self.md_utils.new_header(level=self.level, title="Return")
        contents = ["Type", "Description"]
        contents.extend([
            self.docstring.returns.type, self.docstring.returns.description
        ])
        self.md_utils.new_table(columns=2,
                                rows=2,
                                text=contents,
                                text_align=self.settings.table_align)
