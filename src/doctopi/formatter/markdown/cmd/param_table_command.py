"""The MarkdownParamTableCommand configures a markdown table and
adds it to a markdown generator."""
# pylint: disable = too-few-public-methods

# Built-in imports
from typing import List

# Third-party imports
from mdutils.mdutils import MdUtils

# This package imports
from doctopi.types import Command, MarkdownSettings, NameDescriptionType


class MarkdownParamTableCommand(Command):
    """The MarkdownParamTableCommand is used to define how to document a
    table of parameters. A param table will have columns for Name, Type,
    and Description.

    Attributes:
        md_utils (MdUtils): Markdown file generator
        settings (MarkdownSettings): Markdown generator settings
        table_rows (List[NameDescriptionType]): Table contents
    """
    def __init__(self,
                 md_utils: MdUtils,
                 settings: MarkdownSettings,
                 table_rows: List[NameDescriptionType]):
        self.md_utils = md_utils
        self.settings = settings
        self.table_rows = table_rows

    def execute(self):
        """Add param table to the markdown generator"""
        contents = ["Name", "Type", "Description"]
        for row in self.table_rows:
            contents.extend([
                row.name, row.type, row.description
            ])
        self.md_utils.new_table(columns=3, rows=len(self.table_rows)+1,
                                text=contents,
                                text_align=self.settings.table_align)
