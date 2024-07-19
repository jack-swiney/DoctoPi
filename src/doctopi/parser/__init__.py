import abc
import os
from typing import Union

from doctopi.types import (DocDir, DocFile)


class Parser(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def parse_file(self, file: Union[str, bytes, os.PathLike]) -> DocFile:
        pass

    @abc.abstractmethod
    def parse_dir(self, root: Union[str, bytes, os.PathLike]) -> DocDir:
        pass