"""Base class for Python source parser adapters"""

import abc
import os
from typing import (List, Union)
from doctopi.parser import Parser
from doctopi.types import (ClassDeclaration, Docstring, FunctionDeclaration)


class PythonAdapter(Parser, metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def get_module_docstring(self, file: Union[str, bytes, os.PathLike]) -> Docstring:
        pass

    @abc.abstractmethod
    def get_module_classes(self, file: Union[str, bytes, os.PathLike]) -> List[ClassDeclaration]:
        pass

    @abc.abstractmethod
    def get_module_functions(self,
                             file: Union[str, bytes, os.PathLike]) -> List[FunctionDeclaration]:
        pass
