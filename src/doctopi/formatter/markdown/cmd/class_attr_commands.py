"""The Doctopi MarkdownBuilder class uses the Command design pattern to
let the user customize the documentation for various types. The
MarkdownClassAttrCommand class and child classes are used to document
various attributes of a class."""
# pylint: disable = too-few-public-methods

# Built-in imports
from __future__ import annotations
from typing import (List, Type)

# Third-party imports
from mdutils.mdutils import MdUtils

# This package imports
from doctopi.types import (Command, ClassDeclaration, MarkdownSettings)
from doctopi.formatter.markdown.cmd.param_table_command import MarkdownParamTableCommand
from doctopi.formatter.markdown.cmd.function_command import MarkdownFunctionCommand
from doctopi.formatter.markdown.cmd.docstring_commands import MarkdownDocstringCommand


class MarkdownClassAttrCommand(Command):
    """The MarkdownClassAttrCommand is used to define how to document
    various attributes of a class, like inner classes, methods, etc.

    Attributes:
        md_utils (MdUtils): Markdown file generator
        settings (MarkdownSettings): Markdown generator settings
        level (int): Heading level to write the Class in markdown
        class_ (ClassDeclaration): The class to document
        class_cmds (List[Type[MarkdownClassAttrCommand]]): List of commands
            to execute in order to document smaller pieces of the class,
            such as member variables, inner classes, methods, etc.
        function_cmds (List[Type[MarkdownDocstringCommand]]): List of commands
            to execute in order to document smaller pieces of a
            function. This is needed by the constructor and method
            subcommands.
    """
    # pylint: disable-next = too-many-arguments
    def __init__(self,
                 md_utils: MdUtils,
                 settings: MarkdownSettings,
                 level: int,
                 class_: ClassDeclaration,
                 class_cmds: List[Type[MarkdownClassAttrCommand]],
                 function_cmds: List[Type[MarkdownDocstringCommand]]):
        """Constructor

        Args:
            md_utils (MdUtils): Markdown file generator
            settings (MarkdownSettings): Markdown generator settings
            level (int): Heading level to write the Class in markdown
            class_ (ClassDeclaration): The class to document
            class_cmds (List[Type[MarkdownClassAttrCommand]]): List of
                commands to execute in order to document smaller pieces
                of the class, such as member variables, inner classes,
                methods, etc.
            function_cmds (List[Type[MarkdownDocstringCommand]]): List of
                commands to execute in order to document smaller pieces
                of a function. This is needed by the constructor and
                method subcommands.

        Raises:
            ValueError: The heading level must be between [1,6]
        """
        if not 1 <= level:
            raise ValueError("Level must be between [1,6]")

        self.md_utils = md_utils
        self.settings = settings
        self.level = min(level, 6)  # Can't go any higher than 6, so flatten at 6.
        self.class_ = class_
        self.class_cmds = class_cmds
        self.function_cmds = function_cmds


class MarkdownConstructorCommand(MarkdownClassAttrCommand):
    """The MarkdownConstructorCommand is used to define how to document
    a class constructor.

    Attributes:
        md_utils (MdUtils): Markdown file generator
        level (int): Heading level to write the Class in markdown
        class_ (ClassDeclaration): The class to document
        class_cmds (List[Type[MarkdownClassAttrCommand]]): List of commands
            to execute in order to document smaller pieces of the class,
            such as member variables, inner classes, methods, etc.
        function_cmds (List[Type[MarkdownDocstringCommand]]): List of commands
            to execute in order to document smaller pieces of a
            function. This is needed by the constructor and method
            subcommands.
    """
    def execute(self):
        """Add constructor documentation to the markdown generator"""
        if not self.settings.constructors or not self.class_.constructor:
            return

        constructor = self.class_.constructor
        constructor.name = "Constructor"

        # Python constructor signature is different from other languages.
        # Update the signature to look like it would in use rather than
        # in the source.
        #
        # e.g. convert `def __init__(self, arg1, arg2)` of class MyClass ->
        #              `MyClass(arg1, arg2)`
        constructor.signature = constructor.signature \
            .replace("def __init__(self, ", f"{self.class_.name}(") \
            .replace("def __init__(self)", f"{self.class_.name}()")

        MarkdownFunctionCommand(md_utils=self.md_utils,
                                settings=self.settings,
                                level=self.level,
                                func=constructor,
                                cmds=self.function_cmds).execute()


class MarkdownClassVarCommand(MarkdownClassAttrCommand):
    """The MarkdownClassVarCommand is used to define how to document
    class variables.

    Attributes:
        md_utils (MdUtils): Markdown file generator
        level (int): Heading level to write the Class in markdown
        class_ (ClassDeclaration): The class to document
        class_cmds (List[Type[MarkdownClassAttrCommand]]): List of commands
            to execute in order to document smaller pieces of the class,
            such as member variables, inner classes, methods, etc.
        function_cmds (List[Type[MarkdownDocstringCommand]]): List of commands
            to execute in order to document smaller pieces of a
            function. This is needed by the constructor and method
            subcommands.
    """
    def execute(self):
        """Add class variable documentation to the markdown generator"""
        if self.class_.class_variables and self.settings.class_vars:
            self.md_utils.new_header(level=self.level, title="Class Variables")
            MarkdownParamTableCommand(md_utils=self.md_utils,
                                      settings=self.settings,
                                      table_rows=self.class_.class_variables).execute()


class MarkdownInstanceVarCommand(MarkdownClassAttrCommand):
    """The MarkdownInstanceVarCommand is used to define how to document
    instance variables.

    Attributes:
        md_utils (MdUtils): Markdown file generator
        level (int): Heading level to write the Class in markdown
        class_ (ClassDeclaration): The class to document
        class_cmds (List[Type[MarkdownClassAttrCommand]]): List of commands
            to execute in order to document smaller pieces of the class,
            such as member variables, inner classes, methods, etc.
        function_cmds (List[Type[MarkdownDocstringCommand]]): List of commands
            to execute in order to document smaller pieces of a
            function. This is needed by the constructor and method
            subcommands.
    """
    def execute(self):
        """Add instance variable documentation to the markdown generator"""
        if self.class_.member_variables and self.settings.instance_vars:
            self.md_utils.new_header(level=self.level, title="Member Variables")
            MarkdownParamTableCommand(md_utils=self.md_utils,
                                      settings=self.settings,
                                      table_rows=self.class_.member_variables).execute()


class MarkdownMethodsCommand(MarkdownClassAttrCommand):
    """The MarkdownMethodsCommand is used to define how to
    document class methods.

    Attributes:
        md_utils (MdUtils): Markdown file generator
        level (int): Heading level to write the Class in markdown
        class_ (ClassDeclaration): The class to document
        class_cmds (List[Type[MarkdownClassAttrCommand]]): List of commands
            to execute in order to document smaller pieces of the class,
            such as member variables, inner classes, methods, etc.
        function_cmds (List[Type[MarkdownDocstringCommand]]): List of commands
            to execute in order to document smaller pieces of a
            function. This is needed by the constructor and method
            subcommands.
    """
    def execute(self):
        """Add class method documentation to the markdown generator"""
        if self.class_.member_functions and self.settings.member_functions:
            self.md_utils.new_header(level=self.level, title="Methods")
            for member_function in self.class_.member_functions:
                MarkdownFunctionCommand(md_utils=self.md_utils,
                                        settings=self.settings,
                                        level=self.level+1,
                                        func=member_function,
                                        cmds=self.function_cmds).execute()
