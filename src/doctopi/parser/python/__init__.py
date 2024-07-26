"""Base class for Python source parser adapters"""
# Built-in imports
import os
from typing import (Callable, List, Union)

# Third-party imports
import docspec
from docspec import Module, Class, Function, Variable
from docspec_python import parse_python_module
from docstring_parser.common import DocstringStyle
from docstring_parser import parse

# This package imports
from doctopi.parser import Parser
from doctopi.types import (ClassDeclaration, DocDir, DocFile, Docstring,
                           FunctionDeclaration, NameDescriptionType, AccessType)


class PythonAdapter(Parser):
    """TODO"""

    def __init__(self, docstring_style: DocstringStyle):
        """_summary_

        Args:
            docstring_style (DocstringStyle): _description_
        """
        self.docstring_style = docstring_style

    def parse_file(self, file: Union[str, bytes, os.PathLike]) -> DocFile:
        """_summary_

        Args:
            file (Union[str, bytes, os.PathLike]): _description_

        Returns:
            DocFile: _description_
        """
        return DocFile()  # TODO

    def parse_dir(self, root: Union[str, bytes, os.PathLike]) -> DocDir:
        raise NotImplementedError

    def _parse_module(self, file: Union[str, bytes, os.PathLike]) -> Module:
        """_summary_

        Args:
            file (Union[str, bytes, os.PathLike]): _description_

        Returns:
            Module: _description_
        """
        return parse_python_module(file)

    @staticmethod
    def module_members(member_type: type, convert_func: Callable) -> Callable:
        """_summary_

        Args:
            member_type (type): _description_
            convert_func (Callable): _description_

        Returns:
            Callable: _description_
        """
        def decorator(func: Callable) -> Callable:
            def wrapper(self, module: Module) -> List:
                """_summary_

                Args:
                    module (Module): _description_

                Returns:
                    List: _description_
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
        """_summary_

        Args:
            file (Union[str, bytes, os.PathLike]): _description_

        Returns:
            Docstring: _description_
        """
        return self._get_module_docstring(parse_python_module(file))

    def _get_module_docstring(self, module: Module) -> Docstring:
        """_summary_

        Args:
            module (Module): _description_

        Returns:
            Docstring: _description_
        """
        return self._docspec_to_doctopi_docstring(module.docstring)

    def get_module_classes(self, file: Union[str, bytes, os.PathLike]) -> List[ClassDeclaration]:
        """_summary_

        Args:
            file (Union[str, bytes, os.PathLike]): _description_

        Returns:
            List[ClassDeclaration]: _description_
        """
        return self._get_module_classes(parse_python_module(file))

    @module_members(Class, lambda self, member: self._docspec_to_doctopi_class(member))
    def _get_module_classes(self, module: Module) -> List[ClassDeclaration]:
        """_summary_

        Args:
            module (Module): _description_

        Returns:
            List[ClassDeclaration]: _description_
        """
        # The actual implementation is handled by the decorator

    def get_module_functions(self,
                             file: Union[str, bytes, os.PathLike]) -> List[FunctionDeclaration]:
        """_summary_

        Args:
            file (Union[str, bytes, os.PathLike]): _description_

        Returns:
            List[FunctionDeclaration]: _description_
        """
        return self._get_module_functions(parse_python_module(file))

    @module_members(Function, lambda self, member: self._docspec_to_doctopi_function(member))
    def _get_module_functions(self, module: Module) -> List[FunctionDeclaration]:
        """_summary_

        Args:
            module (Module): _description_

        Returns:
            List[FunctionDeclaration]: _description_
        """
        # The actual implementation is handled by the decorator

    def _docspec_to_doctopi_docstring(self, docstring: docspec.Docstring) -> Docstring:
        """_summary_

        Args:
            docstring (docspec.Docstring): _description_

        Returns:
            Docstring: _description_
        """
        # Set defaults
        summary = ""
        args = []
        returns = None
        raises = []

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


        return Docstring(summary=summary,
                         args=args,
                         returns=returns,
                         raises=raises)

    def _docspec_to_doctopi_function(self, function: Function) -> FunctionDeclaration:
        """_summary_

        Args:
            function (Function): _description_

        Returns:
            FunctionDeclaration: _description_
        """
        return FunctionDeclaration(
            name=function.name,
            signature=self._parse_function_signature(function),
            access=self._parse_access_type(function),
            docstring=self._docspec_to_doctopi_docstring(function.docstring)
        )


    def _docspec_to_doctopi_class(self, cls: Class) -> ClassDeclaration:
        member_variables = []
        member_functions = []
        member_classes = []

        for member in cls.members:
            if isinstance(member, Function):
                member_functions.append(self._docspec_to_doctopi_function(member))

            elif isinstance(member, Class):
                member_functions.append(self._docspec_to_doctopi_class(member))

            elif isinstance(member, Variable):
                member_functions.append(NameDescriptionType(
                    name=member.name,
                    type=member.datatype
                ))

        return ClassDeclaration(
            name=cls.name,
            signature=self._parse_class_signature(cls),
            docstring=self._docspec_to_doctopi_docstring(cls.docstring),
            member_variables=member_variables,
            member_functions=member_functions,
            subclasses=member_classes
        )

    def _parse_function_signature(self, function: Function) -> str:
        """_summary_

        Args:
            function (Function): _description_

        Returns:
            str: _description_
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
        """_summary_

        Args:
            cls (Class): _description_

        Returns:
            str: _description_
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

        # Construct the class signature
        signature = f"{decorators_str}\nclass {class_name}{bases_and_meta}:"

        return signature

    def _parse_access_type(self, function: Function) -> AccessType:
        """For Python, there's no real public, protected, or privates.
        However, according to PEP8:
            _single_leading_underscore: weak “internal use” indicator.
                E.g. from M import * does not import objects whose names
                start with an underscore.

        Args:
            function (Function): _description_

        Returns:
            AccessType: _description_
        """

        return AccessType.PROTECTED if function.name.startswith("_") \
            and not function.name.startswith("__") else AccessType.PUBLIC
