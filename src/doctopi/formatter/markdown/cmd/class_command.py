"""The Doctopi MarkdownBuilder class uses the Command design pattern to
let the user customize the documentation for various types. The
MarkdownClassCommand is used to define how to document a class. It uses
various sub-commands to recursively document inner classes, methods,
etc.
"""
# pylint: disable = too-few-public-methods

# This package imports
from doctopi.formatter.markdown.cmd.class_attr_commands import MarkdownClassAttrCommand


class MarkdownClassCommand(MarkdownClassAttrCommand):
    """The MarkdownClassCommand is used to define how to document a
    class. It uses various sub-commands to recursively document inner
    classes, methods, etc.

    Attributes:
        md_utils (MdUtils): Markdown file generator
        level (int): Heading level to write the Class in markdown
        class_ (ClassDeclaration): The class to document
        class_cmds (List[MarkdownClassAttrCommand]): List of commands
            to execute in order to document smaller pieces of the class,
            such as member variables, inner classes, methods, etc.
        function_cmds (List[MarkdownDocstringCommand]): List of commands
            to execute in order to document smaller pieces of a
            function. This is needed by the constructor and method
            subcommands.
    """
    def execute(self):
        """Add class documentation to the markdown generator"""
        # Overview
        self.md_utils.new_header(level=self.level, title=self.class_.name)
        self.md_utils.insert_code(self.class_.signature, language=self.settings.src_language)
        if self.class_.docstring.summary:
            self.md_utils.new_paragraph(self.class_.docstring.summary)

        # Execute all the sub-commands in the order provided.
        for cmd in self.class_cmds:
            cmd(md_utils=self.md_utils,
                settings=self.settings,
                level=self.level+1,
                class_=self.class_,
                class_cmds=self.class_cmds,
                function_cmds=self.function_cmds).execute()


class MarkdownInnerClassCommand(MarkdownClassAttrCommand):
    """The MarkdownInnerClassCommand is used to define how to document
    an inner class. It uses various sub-commands to recursively document
    additional inner classes, methods, etc.

    Attributes:
        md_utils (MdUtils): Markdown file generator
        level (int): Heading level to write the Class in markdown
        class_ (ClassDeclaration): The class to document
        class_cmds (List[MarkdownClassAttrCommand]): List of commands
            to execute in order to document smaller pieces of the class,
            such as member variables, inner classes, methods, etc.
        function_cmds (List[MarkdownDocstringCommand]): List of commands
            to execute in order to document smaller pieces of a
            function. This is needed by the constructor and method
            subcommands.
    """
    def execute(self):
        """Add inner class documentation to the markdown generator"""
        if self.class_.subclasses and self.settings.inner_classes:
            self.md_utils.new_header(level=self.level, title="Inner Classes")
            for inner_class in self.class_.subclasses:
                MarkdownClassCommand(md_utils=self.md_utils,
                                     settings=self.settings,
                                     level=self.level+1,
                                     class_=inner_class,
                                     class_cmds=self.class_cmds,
                                     function_cmds=self.function_cmds).execute()
