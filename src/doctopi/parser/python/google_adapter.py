import os
from typing import (List, Union)
from doctopi.types import (ClassDeclaration, DocDir, DocFile, Docstring, FunctionDeclaration)
from doctopi.parser.python.python_adapter import PythonAdapter


class GoogleAdapter(PythonAdapter):


    def get_module_docstring(self, file: Union[str, bytes, os.PathLike]) -> Docstring:
        # TODO
        return

    def get_module_classes(self, file: Union[str, bytes, os.PathLike]) -> List[ClassDeclaration]:
        # TODO
        return

    def get_module_functions(self,
                             file: Union[str, bytes, os.PathLike]) -> List[FunctionDeclaration]:
        # TODO
        return

    def parse_file(self, file: Union[str, bytes, os.PathLike]) -> DocFile:
        # TODO
        return

    def parse_dir(self, root: Union[str, bytes, os.PathLike]) -> DocDir:
        # TODO
        return