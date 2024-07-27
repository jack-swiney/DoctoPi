"""The doctopi.parser package leverages the Adapter software design
pattern to adapt third-party tools and APIs for parsing source code
of varying languages, and converts them into doctopi types."""

# Built-in imports
import abc
import os
from typing import Union

# This package imports
from doctopi.types import (DocDir, DocFile)


class Parser(metaclass=abc.ABCMeta):
    """Generic source-code documentation parser. This is an abstract
    base class and is intended to be extended for various programming
    languages, and docstring flavors. The Parser will use the Adapter
    software design pattern to adapt third-party tools and libraries
    like Docspec, Doxygen, and Sphinx to a common documentation parser.
    """

    @abc.abstractmethod
    def parse_file(self, file: Union[str, bytes, os.PathLike]) -> DocFile:
        """To be overidden by the child classes (adapters). Takes a
        source code file and parses it, returning the common doctopi
        DocFile object.

        Args:
            file (Union[str, bytes, os.PathLike]): File to parse.

        Returns:
            DocFile: Representation of the file contents and docstrings.
        """

    @abc.abstractmethod
    def parse_dir(self, root: Union[str, bytes, os.PathLike]) -> DocDir:
        """To be overidden by the child classes (adapters). Takes a
        source code directory and recursively parses it, returning the
        common doctopi DocDir object.

        Args:
            root (Union[str, bytes, os.PathLike]): Source directory to
                walk and parse.

        Returns:
            DocDir: Collection of DocFile and DocDirs  mapping the
                provided directory to the doctopi documentation types.
        """
