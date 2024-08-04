"""Test doctopi.formatter.markdown.cmd.class_attr_commands package"""
# Third-party imports
from mdutils import MdUtils
import pytest

# This package imports
from doctopi.types import (AccessType, ClassDeclaration, Docstring, FunctionDeclaration,
                           MarkdownSettings, NameDescriptionType)
from doctopi.formatter.markdown.cmd.class_attr_commands import (MarkdownConstructorCommand,
                                                                MarkdownClassVarCommand,
                                                                MarkdownInstanceVarCommand,
                                                                MarkdownMethodsCommand)


class TestMarkdownClassAttrCommand:
    """Test doctopi.formatter.markdown.cmd.class_attr_commands package"""

    @pytest.mark.parametrize("command", [MarkdownConstructorCommand, MarkdownClassVarCommand,
                                         MarkdownInstanceVarCommand, MarkdownMethodsCommand])
    @pytest.mark.parametrize("level,err,set_level", [
        (0, True, 0), (1, False, 1), (2, False, 2), (3, False, 3),
        (4, False, 4), (5, False, 5), (6, False, 6), (7, False, 6),
        (1_000_000, False, 6), (-1, True, 0), (-1_000_000, True, 0)
    ])
    def test_markdown_class_attr_command(self, command, level, err, set_level):
        """Verify the MarkdownClassAttrCommand setter handles various md
        heading levels
        """
        if err:
            with pytest.raises(ValueError):
                command(md_utils=None, settings=None, level=level,
                        class_=None, class_cmds=[], function_cmds=[])

        else:
            cmd = command(md_utils=None, settings=None, level=level,
                          class_=None, class_cmds=[], function_cmds=[])
            assert cmd.level == set_level

    @pytest.mark.parametrize("command,mock", [
        (MarkdownConstructorCommand, "MarkdownFunctionCommand"),
        (MarkdownClassVarCommand, "MarkdownParamTableCommand"),
        (MarkdownInstanceVarCommand, "MarkdownParamTableCommand"),
        (MarkdownMethodsCommand, "MarkdownFunctionCommand")])
    def test_cmd_execute(self, mocker, command, mock):
        """Execute a MarkdownClassAttrCommand"""
        # Create a test class
        class_ = ClassDeclaration("MyClass",
                                  "class MyClass:",
                                  Docstring(summary="My test class",
                                            args=[],
                                            raises=[],
                                            returns=None),
                                  constructor=FunctionDeclaration("__init__",
                                                                  "def __init__(self):",
                                                                  access=AccessType.PUBLIC,
                                                                  docstring=Docstring()),
                                  class_variables=[NameDescriptionType(name="MyClassVar",
                                                                       description="_description_",
                                                                       type="str")],
                                  member_variables=[NameDescriptionType(name="MyMemberVar",
                                                                        description="_description_",
                                                                        type="int")],
                                  methods=[FunctionDeclaration("my_method",
                                                               signature="def my_method(self):",
                                                               access=AccessType.PUBLIC),
                                           FunctionDeclaration("_my_method",
                                                               signature="def _my_method(self):",
                                                               access=AccessType.PROTECTED)])

        settings = MarkdownSettings()

        mocker.patch(f"doctopi.formatter.markdown.cmd.class_attr_commands.{mock}")
        mock_mdutils = mocker.Mock(spec=MdUtils)

        cmd = command(md_utils=mock_mdutils,
                      settings=settings,
                      level=3,
                      class_=class_,
                      class_cmds=[],
                      function_cmds=[])

        cmd.execute()

        # Verify MarkdownConstructorCommand.execute() returns early if
        # settings.constructors isn't set
        if isinstance(cmd, MarkdownConstructorCommand):
            cmd.settings.constructors = False
            cmd.execute()
