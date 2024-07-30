"""Adapter to convert docspec utilites/types to doctopi types. Used to
parse Python source code with Google, Numpy, EpyDoc, or Sphinx style
docstrings.
"""
# Built-in imports
import logging
import os
from typing import (Callable, List, Union)

# Third-party imports
import docspec
from docspec import Module, Class, Function, Variable
from docspec_python import parse_python_module
from docstring_parser.common import DocstringStyle, ParseError
from docstring_parser import parse

# This package imports
from doctopi.parser import Parser
from doctopi.types import (ClassDeclaration, DocDir, DocFile, Docstring,
                           FunctionDeclaration, NameDescriptionType, AccessType)


class DocspecAdapter(Parser):
    """Adapter to convert docspec utilites/types to doctopi types. Used to
    parse Python source code with Google, Numpy, EpyDoc, or Sphinx style
    docstrings.

    Args:
        docstring_style (docstring_parser.common.DocstringStyle):
            Use the DocstringStyle enum to toggle which type of
            docstring format to parse.
    """

    def __init__(self, docstring_style: DocstringStyle):
        """Constructor

        Args:
            docstring_style (docstring_parser.common.DocstringStyle):
                Use the DocstringStyle enum to toggle which type of
                docstring format to parse.
        """
        self.docstring_style = docstring_style

    def parse_file(self, file: Union[str, bytes, os.PathLike]) -> DocFile:
        """Parse a Python file and return a doctopi.DocFile object
        representing the contents/docstrings.

        Args:
            file (Union[str, bytes, os.PathLike]): File to parse

        Returns:
            DocFile: Representation of the file contents and docstrings
        """
        # Parse the module
        module: Module = parse_python_module(file)

        # docspec_python converts __init__ files to the name of the
        # package, which makes sense but doesn't work for this adapter
        if file.endswith("__init__.py"):
            module.name = "__init__"

        # Instantiate and return a DocFile using helper methods
        return DocFile(
            name=module.name,
            path=os.path.abspath(file),
            docstring=self._get_module_docstring(module),
            classes=self._get_module_classes(module),
            functions=self._get_module_functions(module)
        )

    def parse_dir(self, root: Union[str, bytes, os.PathLike]) -> DocDir:
        """Walk a directory and parse the contents/docstrings of each
        module

        Args:
            root (Union[str, bytes, os.PathLike]): Source directory to
                walk and parse.

        Returns:
            DocDir: Collection of DocFile and DocDirs  mapping the
                provided directory to the doctopi documentation types.
        """
        # Get all of the items in the root directory
        entries = os.listdir(root)

        # Initialize lists of DocDir (subdirectories) and DocFiles (modules)
        dirs = []
        modules = []

        # Check the type of each item in the root directory
        for entry in entries:
            full_path = os.path.join(root, entry)

            # Recursively parse the subdirectory
            if os.path.isdir(full_path):
                dirs.append(self.parse_dir(full_path))

            # Parse Python modules
            elif os.path.isfile(full_path) and full_path.endswith(".py"):
                modules.append(self.parse_file(full_path))

       # Instantiate and return a DocDir representing the root
        return DocDir(
            name=os.path.basename(os.path.normpath(root)),
            path=os.path.abspath(root),
            files=modules,
            subdirs=dirs
        )

    @staticmethod
    def module_members(member_type: type, convert_func: Callable) -> Callable:
        """Decorator function for converting types from a dospec Module
        into a list of doctopi types.

        Args:
            member_type (type): type in docspec.Module.members to
                convert to doctopi type.
            convert_func (Callable): function for converting the docspec
                module members of member_type to a doctopi type.

        Returns:
            Callable: Decorators return a Callable that wraps the
                function or class it decorates. See below for details
                on what is returned by the Callable itself.
        """
        def decorator(func: Callable) -> Callable:  # pylint: disable=unused-argument
            """Execute the wrapper function below whenver a function
            is decorated with this module_members decorator.

            Args:
                func (Callable): Function that is decorated. This
                    function shouldn't implement any functionality, as
                    the decorator will handle it all. The function
                    being decorator will just be a convenient name/
                    entrypoint for this decorator function

            Returns:
                Callable: Decorators return a Callable that wraps the
                    function or class it decorates. See below for
                    details on what is returned by the Callable itself.
            """
            def wrapper(self, module: Module) -> List:
                """Convert types from a dospec Module into a list of
                doctopi types.

                Args:
                    module (Module): Python module that has been parsed
                        by docspec

                Returns:
                    List: list of doctopi types specified in the
                        decorator arguments, converted from the dospec
                        Module.
                """
                # Create a list of declarations
                declarations = []

                # Go through each member and filter by the specified type
                for member in module.members:
                    if isinstance(member, member_type):
                        declarations.append(convert_func(self, member))

                return declarations
            return wrapper
        return decorator

    def get_module_docstring(self, file: Union[str, bytes, os.PathLike]) -> Docstring:
        """Use the docspec adapter to parse a Python module and return
        its docstring

        Args:
            file (Union[str, bytes, os.PathLike]): Python module

        Returns:
            Docstring: Python module's docstring
        """
        return self._get_module_docstring(parse_python_module(file))

    def _get_module_docstring(self, module: Module) -> Docstring:
        """Provided docspec has already parsed a module, use the adapter
        to convert from docspec types to doctopi types, and return the
        docstring of the module

        Args:
            module (Module): Python module

        Returns:
            Docstring: Python module's docstring
        """
        return self._docspec_to_doctopi_docstring(module.docstring)

    def get_module_classes(self, file: Union[str, bytes, os.PathLike]) -> List[ClassDeclaration]:
        """Use the docspec adapter to parse a Python module and return
        its classes

        Args:
            file (Union[str, bytes, os.PathLike]): Python module

        Returns:
            List[ClassDeclaration]: list of classes in the Python module
        """
        return self._get_module_classes(parse_python_module(file))

    @module_members(Class, lambda self, member: self._docspec_to_doctopi_class(member))
    def _get_module_classes(self, module: Module) -> List[ClassDeclaration]:
        """Provided docspec has already parsed a module, use the adapter
        to convert from docspec types to doctopi types, and return the
        classes in the Python module

        Args:
            module (Module): Python module

        Returns:
            List[ClassDeclaration]: list of classes in the Python module
        """
        # The actual implementation is handled by the decorator

    def get_module_functions(self,
                             file: Union[str, bytes, os.PathLike]) -> List[FunctionDeclaration]:
        """Use the docspec adapter to parse a Python module and return
        its functions

        Args:
            file (Union[str, bytes, os.PathLike]): Python module

        Returns:
            List[FunctionDeclaration]: list of functions in the Python
            module
        """
        return self._get_module_functions(parse_python_module(file))

    @module_members(Function, lambda self, member: self._docspec_to_doctopi_function(member))
    def _get_module_functions(self, module: Module) -> List[FunctionDeclaration]:
        """Provided docspec has already parsed a module, use the adapter
        to convert from docspec types to doctopi types, and return the
        functions in the Python module

        Args:
            module (Module): Python module

        Returns:
            List[FunctionDeclaration]: list of functions in Python
            module
        """
        # The actual implementation is handled by the decorator

    def _docspec_to_doctopi_docstring(self, docstring: docspec.Docstring) -> Docstring:
        """Convert a docspec.Docstring type into a doctopi.Docstring

        Args:
            docstring (docspec.Docstring): docspec representation of
                a docstring

        Returns:
            Docstring: doctopi representation of a docstring
        """
        # Set defaults
        summary = ""
        args = []
        returns = None
        raises = []

        try:
            if docstring:
                parsed_docstring = parse(docstring.content, style=self.docstring_style)
                summary = parsed_docstring.description

                # Convert each docspec.DocstringParam to a doctopi.NameDescriptionType
                for arg in parsed_docstring.params:
                    args.append(
                        NameDescriptionType(
                            name=arg.arg_name,
                            description=arg.description,
                            type=arg.type_name
                        )
                    )

                # Convert the docspec.DocstringReturns to a doctopi.NameDescriptionType
                if parsed_docstring.returns:
                    returns = NameDescriptionType(
                        description=parsed_docstring.returns.description,
                        type=parsed_docstring.returns.type_name
                    )

                # Convert each docspec.DocstringRaises to a doctopi.NameDescriptionType
                for exc in parsed_docstring.raises:
                    raises.append(
                        NameDescriptionType(
                            description=exc.description,
                            type=exc.type_name
                        )
                    )

        # Docspec will throw a ParseError if the docstring isn't in the flavor
        # specified. DocstringStyle.AUTO should be used for atypical styles
        except ParseError:
            logging.warning("Failed to parse %s for style %s",
                            docstring.location, self.docstring_style)

        # Convert to doctopi.Docstring
        return Docstring(summary=summary,
                         args=args,
                         returns=returns,
                         raises=raises)

    def _docspec_to_doctopi_function(self, function: Function) -> FunctionDeclaration:
        """Convert a docspec.Function type into a
        doctopi.FunctionDeclaration

        Args:
            function (Function): docspec representation of a function

        Returns:
            FunctionDeclaration: doctopi representation of a function
        """
        return FunctionDeclaration(
            name=function.name,
            signature=self._parse_function_signature(function),
            access=self._parse_access_type(function),
            docstring=self._docspec_to_doctopi_docstring(function.docstring)
        )

    def _docspec_to_doctopi_class(self, cls: Class) -> ClassDeclaration:
        """convert a docspec.Class type into a doctopi.ClassDeclaration

        Args:
            cls (Class): docspec representation of a class

        Returns:
            ClassDeclaration: doctopi representation of a class
        """
        class_variables = []
        member_variables = []
        member_functions = []
        member_classes = []
        constructor = None

        # Go through all of the class members
        for member in cls.members:

            # Convert member functions
            if isinstance(member, Function):
                function_declaration = self._docspec_to_doctopi_function(member)
                # Separate the constructor from the member functions
                if function_declaration.name == "__init__":
                    constructor = function_declaration
                else:
                    member_functions.append(function_declaration)

            # Convert subclasses
            elif isinstance(member, Class):
                member_classes.append(self._docspec_to_doctopi_class(member))

            # Convert class variables
            elif isinstance(member, Variable):
                class_variables.append(NameDescriptionType(
                    name=member.name,
                    type=member.datatype
                ))

        # Convert member variables from docstring
        if cls.docstring:
            parsed_docstring = parse(cls.docstring.content, style=self.docstring_style)
            for member_var in parsed_docstring.params:
                member_variables.append(NameDescriptionType(
                    name=member_var.arg_name,
                    type=member_var.type_name,
                    description=member_var.description
                ))

        # Convert the docspec.Class to doctopi.ClassDeclaration
        return ClassDeclaration(
            name=cls.name,
            signature=self._parse_class_signature(cls),
            constructor=constructor,
            docstring=self._docspec_to_doctopi_docstring(cls.docstring),
            class_variables=class_variables,
            member_variables=member_variables,
            member_functions=member_functions,
            subclasses=member_classes
        )

    def _parse_function_signature(self, function: Function) -> str:
        """Take a docspec.Function object and put together the original
        function's signature like it's written in the source code.

        Args:
            function (Function): docspec representation of a Function

        Returns:
            str: function's signature
        """
        # Extract the function name
        func_name = function.name

        # Extract the parameters
        params = []
        for param in function.args:
            param_str = ""

            # Decide if asterisks are needed
            if param.type.value == 2:
                param_str += f"*{param.name}"
            elif param.type.value == 4:
                param_str += f"**{param.name}"
            else:
                param_str += param.name

            # Append typehints if provided
            if param.datatype:
                param_str += f": {param.datatype}"

            # Append defaults if provided
            if param.default_value:
                param_str += f" = {param.default_value}"

            params.append(param_str)

        # Join parameters with commas
        params_str = ", ".join(params)

        # Extract the return type
        return_type = f" -> {function.return_type}" if function.return_type else ""

        # Construct the function signature
        return f"def {func_name}({params_str}){return_type}:"

    def _parse_class_signature(self, cls: Class) -> str:
        """Take a docspec.Class object and put together the original
        class's signature like it's written in the source code.

        Args:
            cls (Class): docspec representation of a class

        Returns:
            str: class's signature
        """
        # Extract the class name
        class_name = cls.name

        # Extract the parent classes
        bases = cls.bases or []
        bases_str = ", ".join(bases)

        # Extract the metaclass (if any)
        metaclass_str = ""
        if cls.metaclass:
            metaclass_str = f", metaclass={cls.metaclass}"

        # Construct the base and metaclass part of the class definition
        if bases_str or metaclass_str:
            bases_and_meta = f"({bases_str}{metaclass_str})"
        else:
            bases_and_meta = ""

        # Extract decorators
        decorators = cls.decorations or []
        decorators_str = "\n".join(f"@{dec.name}" for dec in decorators)
        dec_newline = "\n" if decorators_str else ""

        # Construct the class signature
        signature = f"{decorators_str}{dec_newline}class {class_name}{bases_and_meta}:"

        return signature

    def _parse_access_type(self, function: Function) -> AccessType:
        """For Python, there's no real public, protected, or privates.
        However, according to PEP8:
            _single_leading_underscore: weak “internal use” indicator.
                E.g. from M import * does not import objects whose names
                start with an underscore.

        Args:
            function (Function): docspec representation of a function

        Returns:
            AccessType: Enum of public, private, or protected.
        """

        return AccessType.PROTECTED if function.name.startswith("_") \
            and not function.name.startswith("__") else AccessType.PUBLIC
