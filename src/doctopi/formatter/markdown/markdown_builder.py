"""The MarkdownBuilder configures and generates documentation in
Markdown
"""
# Built-in imports
from __future__ import annotations
import os
from typing import (List, Type, Union)

# Third-party imports
from mdutils import MdUtils

# This package imports
from doctopi.formatter.markdown.cmd.class_command import (MarkdownClassCommand,
                                                          MarkdownClassAttrCommand)
from doctopi.formatter.markdown.cmd.function_command import (MarkdownDocstringCommand,
                                                             MarkdownFunctionCommand)
from doctopi.parser import Parser
from doctopi.parser.parser_factory import ParserFactory
from doctopi.types import Command, DocDir, DocFile, MarkdownSettings

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
        title (str): Title of the markdown document to create. Default
            is None.
        author (str): Author of the markdown document to create. Default
             is None.
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
        public_only (bool): If enabled, only public class
            methods will be documented.
    """
    def __init__(self):
        """Constructor"""
        # Generic
        self.src_language: str = ""  # python, java, or cpp
        self.parser: Parser = None
        self.src: Union[str, bytes, os.PathLike] = ""
        self.output: str = ""
        self.recursive: bool = False

        # Metadata
        self.title: str = ""
        self.author: str = ""

        # Command pattern
        self.file_commands: List[Type[Command]] = []
        self.class_commands: List[Type[MarkdownClassAttrCommand]] = []
        self.function_commands: List[Type[MarkdownDocstringCommand]] = []

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
        self.public_only: bool = True

    def build(self):
        """Generate the markdown by executing the provided commands
        """
        # Initialize the md file
        md_utils = MdUtils(file_name=self.output, title=self.title, author=self.author)

        # Parse the provided source path
        parsed_docs: Union[DocFile, DocDir] = self.parser.parse_file(self.src) \
             if os.path.isfile(self.src) else self.parser.parse_dir(self.src)

        # Build a single file if it's a single file
        if isinstance(parsed_docs, DocFile):
            self.build_single_file(md_utils=md_utils, level=1, parsed_file=parsed_docs)

        # Build for multiple files if it's a dir
        else:
            self.build_dir(md_utils=md_utils, level=1, parsed_dir=parsed_docs)

        # Create a table of contents
        if self.table_of_contents:
            md_utils.new_table_of_contents(table_title=self.toc_title, depth=self.toc_depth)

        # Output the file.
        md_utils.create_md_file()


    def build_dir(self, md_utils: MdUtils, level: int, parsed_dir: DocDir):
        """Generate the markdown of a directory by executing the
        provided commands

        Args:
            md_utils (MdUtils): Markdown file generator
            level (int): Starting heading level to build the provided
                file's documentation
            parsed_dir (DocDir): parsed source directory
        """
        # If using recursion, need an extra level for the directory header
        file_level = level + 1
        if self.recursive:
            file_level = level + 2
            md_utils.new_header(level=level, title=f"{parsed_dir.name}/")

        for doc in parsed_dir.files:
            # Create a header for the name of the individual file
            md_utils.new_header(level=file_level-1, title=doc.name)
            # Build each individual file
            self.build_single_file(md_utils=md_utils, level=file_level, parsed_file=doc)

        if self.recursive:
            # If set to recursive mode, build a directory one level lower for each subdir.
            for subdir in parsed_dir.subdirs:
                self.build_dir(md_utils=md_utils, level=level+1, parsed_dir=subdir)

    def build_single_file(self, md_utils: MdUtils, level: int, parsed_file: DocFile):
        """Generate the markdown of a single file by executing the
        provided commands

        Args:
            md_utils (MdUtils): Markdown file generator
            level (int): Starting heading level to build the provided
                file's documentation
            parsed_file (DocFile): parsed source file
        """
        # Create an overview section
        if self.file_overview and parsed_file.docstring.summary:
            md_utils.new_header(level=level, title='Overview')
            md_utils.new_paragraph(parsed_file.docstring.summary)
            md_utils.new_paragraph()

        settings = MarkdownSettings(
            src_language=self.src_language,
            table_align=self.table_align,
            table_of_contents=self.table_of_contents,
            constructors=self.constructors,
            class_vars=self.class_vars,
            instance_vars=self.instance_vars,
            inner_classes=self.inner_classes,
            member_functions=self.member_functions,
            file_overview=self.file_overview,
            public_only=self.public_only
        )

        # Generate sections in order of the provided commands
        for command in self.file_commands:
            # Create a "Classes" section
            if issubclass(command, MarkdownClassCommand):
                if parsed_file.classes:
                    md_utils.new_header(level=level, title='Classes')

                # Pass configuration to the command and execute
                for class_ in parsed_file.classes:
                    command(md_utils=md_utils,
                            settings = settings,
                            level=level+1,
                            class_ = class_,
                            class_cmds = self.class_commands,
                            function_cmds = self.function_commands).execute()

            # Create a "Functions" section
            elif issubclass(command, MarkdownFunctionCommand):
                if parsed_file.functions:
                    md_utils.new_header(level=level, title='Functions')

                # Pass configuration to the command and execute
                for function in parsed_file.functions:
                    command(md_utils=md_utils,
                            settings = settings,
                            level=level+1,
                            func = function,
                            cmds = self.function_commands).execute()

    def add_file_command(self, command: Type[Command]) -> MarkdownBuilder:
        """Add a Markdown generation command. Upon calling
        MarkdownBuild.build(), commands will be executed one by one
        to format and generate documentation in markdown.

        Args:
            command (Type[Command]): Commands to execute at the file
                level

        Returns:
            MarkdownBuilder: This MarkdownBuilder
        """
        self.file_commands.append(command)
        return self

    def add_class_commands(self, command: Type[MarkdownClassAttrCommand]) -> MarkdownBuilder:
        """Add a Markdown generation command. Upon calling
        MarkdownBuild.build(), commands will be executed one by one
        to format and generate documentation in markdown.

        Args:
            command (Type[Command]): Commands to execute at the class
                level

        Returns:
            MarkdownBuilder: This MarkdownBuilder
        """
        self.class_commands.append(command)
        return self

    def add_function_commands(self, command: Type[MarkdownDocstringCommand]) -> MarkdownBuilder:
        """Add a Markdown generation command. Upon calling
        MarkdownBuild.build(), commands will be executed one by one
        to format and generate documentation in markdown.

        Args:
            command (Type[Command]): Commands to execute at the function
                level

        Returns:
            MarkdownBuilder: This MarkdownBuilder
        """
        self.function_commands.append(command)
        return self

    def configure_metadata(self, title: str = "", author: str = "") -> MarkdownBuilder:
        """Configure Markdown file metadata

        Args:
            title (str, optional): Title of the markdown document to
                create. Defaults to "".
            author (str, optional): Author of the markdown document to
                create. Defaults to "".

        Returns:
            MarkdownBuilder: This MarkdownBuilder
        """
        self.title = title
        self.author = author
        return self

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
                     output: str = "README.md",
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
