"""TODO"""
# Built-in imports
from typing import List

# Third-party imports
from mdutils.mdutils import MdUtils
from doctopi.types import FunctionDeclaration, NameDescriptionType, ClassDeclaration

# This package imports
from doctopi.parser.parser_factory import ParserFactory


TEST_FILE = "../../../tests/example_google.py"


class MarkdownFormatter:
    """Generate a markdown file from the TEST_FILE"""
    def __init__(self):
        """Generate a markdown file from the TEST_FILE"""
        self.generate_md_file(TEST_FILE)

    def _md_name_type_description_table(self, md_utils: MdUtils, rows: List[NameDescriptionType]):
        """_summary_

        Args:
            md_utils (MdUtils): _description_
            rows (List[NameDescriptionType]): _description_
        """
        contents = ["Name", "Type", "Description"]
        for row in rows:
            contents.extend([
                row.name, row.type, row.description
            ])
        md_utils.new_table(columns=3, rows=len(rows)+1,
                            text=contents,
                            text_align='left')

    def _md_function(self, md_utils: MdUtils, func: FunctionDeclaration, level: int = 2):
        """_summary_

        Args:
            md_utils (MdUtils): _description_
            func (FunctionDeclaration): _description_
            level (int, optional): _description_. Defaults to 2.
        """
        # Header with function signature
        md_utils.new_header(level=level, title=func.name)
        md_utils.insert_code(
            func.signature,
            language="python"
        )
        # Include the summary/description
        if func.docstring:
            md_utils.new_paragraph(func.docstring.summary)

            # Args header with table of args
            if func.docstring.args:
                md_utils.new_header(level=level+1, title="Args")
                self._md_name_type_description_table(md_utils, func.docstring.args)

            # Raises header with table of exceptions
            if func.docstring.raises:
                md_utils.new_header(level=level+1, title="Raises")
                self._md_name_type_description_table(md_utils, func.docstring.raises)

            # Returns header with table of return
            if func.docstring.returns:
                md_utils.new_header(level=level+1, title="Return")
                contents = ["Type", "Description"]
                contents.extend([
                    func.docstring.returns.type, func.docstring.returns.description
                ])
                md_utils.new_table(columns=2, rows=2,
                                    text=contents,
                                    text_align='left')

    def _md_class(self, md_utils: MdUtils, class_: ClassDeclaration, level: int = 2):
        """_summary_

        Args:
            md_utils (MdUtils): _description_
            class_ (ClassDeclaration): _description_
            level (int, optional): _description_. Defaults to 2.
        """
        # Overview
        md_utils.new_header(level=level, title=class_.name)
        md_utils.insert_code(class_.signature, language="python")
        md_utils.new_paragraph(class_.docstring.summary)

        # Constructor
        if class_.constructor:
            constructor = class_.constructor
            constructor.name = "Constructor"
            constructor.signature = constructor.signature.replace("def __init__(self, ", f"{class_.name}(")
            self._md_function(md_utils, constructor, level=level+1)

        # Class variables
        if class_.class_variables:
            md_utils.new_header(level=level+1, title="Class Variables")
            self._md_name_type_description_table(md_utils, class_.class_variables)

        # Member variables
        if class_.member_variables:
            md_utils.new_header(level=level+1, title="Member Variables")
            self._md_name_type_description_table(md_utils, class_.member_variables)

        # Inner classes
        if class_.subclasses:
            md_utils.new_header(level=level+1, title="Inner Classes")
            for inner_class in class_.subclasses:
                self._md_class(md_utils, inner_class, level=level+2)

        # Functions
        if class_.member_functions:
            md_utils.new_header(level=level+1, title="Member Functions")
            for member_function in class_.member_functions:
                self._md_function(md_utils, member_function, level=level+2)

    def generate_md_file(self, file: str = TEST_FILE):
        """_summary_

        Args:
            file (str, optional): _description_. Defaults to TEST_FILE.
        """
        # Parse the source file
        parsed_file = ParserFactory(language="python", style="google").parse_file(file)

        # Initialize the md file
        md_utils = MdUtils(file_name='tmp_md', title=parsed_file.name)

        # Create an overview section
        md_utils.new_header(level=1, title='Overview')
        md_utils.new_paragraph(parsed_file.docstring.summary)
        md_utils.new_paragraph()

        # Create a "Classes" section
        md_utils.new_header(level=1, title='Classes')
        for class_ in parsed_file.classes:
            self._md_class(md_utils, class_, level=2)

        # Create a table of contents
        md_utils.new_table_of_contents(table_title='Contents', depth=4)
        md_utils.create_md_file()
