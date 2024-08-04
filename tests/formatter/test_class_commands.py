"""Test doctopi.formatter.markdown.cmd.class_command package"""
# Third-party imports
from mdutils import MdUtils
import pytest

# This package imports
from doctopi.types import (AccessType, ClassDeclaration, Docstring, FunctionDeclaration,
                           MarkdownSettings, NameDescriptionType)
from doctopi.formatter.markdown.cmd.class_command import (MarkdownClassCommand,
                                                          MarkdownInnerClassCommand)
from doctopi.formatter.markdown.cmd.class_attr_commands import MarkdownMethodsCommand


class TestMarkdownClassCommands:
    """Test doctopi.formatter.markdown.cmd.class_command package"""

    @pytest.mark.parametrize("command", [MarkdownClassCommand, MarkdownInnerClassCommand])
    def test_cmd_execute(self, mocker, command):
        """Execute a MarkdownClassAttrCommand"""
        # Mocks
        mock_class_attr_cmd = mocker.Mock(spec=MarkdownMethodsCommand)
        mock_mdutils = mocker.Mock(spec=MdUtils)

        # Create a test class
        subclass = ClassDeclaration("MyClass",
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
                                                               access=AccessType.PROTECTED)],
                                  subclasses=[subclass])

        settings = MarkdownSettings()

        cmd = command(md_utils=mock_mdutils,
                      settings=settings,
                      level=3,
                      class_=class_,
                      class_cmds=[mock_class_attr_cmd],
                      function_cmds=[])

        cmd.execute()
