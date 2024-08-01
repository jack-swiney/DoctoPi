"""Test doctopi.formatter.markdown.cmd.function_command package"""
# Third-party imports
from mdutils import MdUtils
import pytest

# This package imports
from doctopi.types import (AccessType, Docstring, FunctionDeclaration, MarkdownSettings)
from doctopi.formatter.markdown.cmd.function_command import MarkdownFunctionCommand
from doctopi.formatter.markdown.cmd.docstring_commands import (MarkdownArgsCommand,
                                                               MarkdownRaisesCommand,
                                                               MarkdownReturnsCommand)


class TestMarkdownFunctionCommand:
    """Test doctopi.formatter.markdown.cmd.function_command package"""

    @pytest.mark.parametrize("access", [AccessType.PROTECTED, AccessType.PUBLIC])
    @pytest.mark.parametrize("level,err,set_level", [
        (0, True, 0), (1, False, 1), (2, False, 2), (3, False, 3),
        (4, False, 4), (5, False, 5), (6, False, 6), (7, False, 6),
        (1_000_000, False, 6), (-1, True, 0), (-1_000_000, True, 0)
    ])
    def test_markdown_class_attr_command(self, mocker, access, level, err, set_level):
        """Verify the MarkdownClassAttrCommand setter handles various md
        heading levels
        """
        if err:
            # Verify a ValueError is raised if a bad level is set
            with pytest.raises(ValueError):
                MarkdownFunctionCommand(md_utils=None,
                                        settings=None,
                                        level=level,
                                        func=None,
                                        cmds=[])

        else:
            # Mock MdUtils
            mock_mdutils = mocker.Mock(spec=MdUtils)

            function_declaration = FunctionDeclaration(name="my_function",
                                                       signature="def my_function(*args, **kwargs)",
                                                       access=access,
                                                       docstring=Docstring(summary="_summary",
                                                                           args=[],
                                                                           returns = None))

            cmds = [MarkdownArgsCommand, MarkdownRaisesCommand, MarkdownReturnsCommand]

            # Instantiate the command
            cmd = MarkdownFunctionCommand(md_utils=mock_mdutils,
                                          settings=MarkdownSettings(),
                                          level=level,
                                          func=function_declaration,
                                          cmds=cmds)
            assert cmd.level == set_level

            # Execute the command
            cmd.execute()
