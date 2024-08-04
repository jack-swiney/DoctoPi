"""Test doctopi.formatter.markdown.cmd.docstring_commands package"""
# Third-party imports
from mdutils import MdUtils
import pytest

# This package imports
from doctopi.types import (Docstring, MarkdownSettings, NameDescriptionType)
from doctopi.formatter.markdown.cmd.docstring_commands import (MarkdownArgsCommand,
                                                               MarkdownRaisesCommand,
                                                               MarkdownReturnsCommand)


class TestMarkdownDocstringCommands:
    """Test doctopi.formatter.markdown.cmd.docstring_commands package"""

    @pytest.mark.parametrize("command", [MarkdownArgsCommand, MarkdownRaisesCommand,
                                         MarkdownReturnsCommand])
    @pytest.mark.parametrize("level,err,set_level", [
        (0, True, 0), (1, False, 1), (2, False, 2), (3, False, 3),
        (4, False, 4), (5, False, 5), (6, False, 6), (7, False, 6),
        (1_000_000, False, 6), (-1, True, 0), (-1_000_000, True, 0)
    ])
    def test_docstring_commands(self, mocker, command, level, err, set_level):
        """Verify the MarkdownDocstringCommands setter handles various md
        heading levels and execute the commands
        """
        if err:
            # Verify a ValueError is raised if a bad level is set
            with pytest.raises(ValueError):
                command(md_utils=None, settings=None, level=level, docstring=None)

        else:
            # Mock MdUtils
            mock_mdutils = mocker.Mock(spec=MdUtils)

            # Create a fake docstring
            docstring = Docstring(summary="_summary_",
                                  args=[NameDescriptionType("arg1", "_description_", "str"),
                                        NameDescriptionType("arg2", "_description_", "int")],
                                  raises=[NameDescriptionType("", "_description_", "ValueError"),
                                          NameDescriptionType("", "_description_", "KeyError")],
                                  returns=NameDescriptionType("", "_description_", "MyCustomType"))

            # Instantiate the command
            cmd = command(md_utils=mock_mdutils,
                          settings=MarkdownSettings(),
                          level=level,
                          docstring=docstring)
            assert cmd.level == set_level

            # Execute the command
            cmd.execute()
