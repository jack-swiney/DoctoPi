"""Common types used by the doctopi package"""
# pylint: disable = too-many-instance-attributes

# Built-in imports
from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
import os
from typing import (List, Union)


class AccessType(Enum):
    """Enum of a class or function's access modifier"""
    PUBLIC = 1
    PROTECTED = 2
    PRIVATE = 3


@dataclass
class NameDescriptionType:
    """Data container for Name, Description, and Type used to describe
    params, returns, members, etc.
    """
    name: str = ""
    description: str = ""
    type: str = ""

    def __post_init__(self):
        """Clean the input types of newlines"""
        self.name = self._strip_newlines(self.name)
        self.description = self._strip_newlines(self.description)
        self.type = self._strip_newlines(self.type)

    def _strip_newlines(self, line: str) -> str:
        """Strip any newlines from a string

        Args:
            line (str): any string

        Returns:
            str: provided string with newlines removed
        """
        return ' '.join(line.splitlines()) if line else line


@dataclass
class Docstring:
    """Doctopi representation of a docstring"""
    summary: str = ""
    args: List[NameDescriptionType] = field(default_factory=list)
    returns: NameDescriptionType = None
    raises: List[NameDescriptionType] = field(default_factory=list)


@dataclass
class FunctionDeclaration:
    """Doctopi representation of a function"""
    name: str
    signature: str
    access: AccessType
    docstring: Docstring = None


@dataclass
class ClassDeclaration:  # pylint: disable = too-many-instance-attributes
    """Doctopi representation of a class"""
    name: str
    signature: str
    docstring: Docstring = None
    constructor: FunctionDeclaration = None
    class_variables: List[NameDescriptionType] = field(default_factory=list)
    member_variables: List[NameDescriptionType] = field(default_factory=list)
    methods: List[FunctionDeclaration] = field(default_factory=list)
    subclasses: List[ClassDeclaration] = field(default_factory=list)


@dataclass
class DocFile:
    """Doctopi representation of a source code file"""
    name: str
    path: Union[str, bytes, os.PathLike]
    docstring: Docstring = None
    classes: List[ClassDeclaration] = field(default_factory=list)
    functions: List[FunctionDeclaration] = field(default_factory=list)


@dataclass
class DocDir:
    """Doctopi representation of a source code directory"""
    name: str
    path: Union[str, bytes, os.PathLike]
    files: List[DocFile] = field(default_factory=list)
    subdirs: List[DocDir] = field(default_factory=list)


# pylint: disable = too-few-public-methods
class Command(ABC):
    """Generic class for the command design pattern"""
    @abstractmethod
    def execute(self):
        """Execute the command"""


@dataclass
class MarkdownSettings:
    """Dataclass to hold Markdown content settings"""
    # Generic
    src_language: str = ""

    # Tables
    table_align: str = "left"  # left, center, or right

    # Enabled content
    table_of_contents: bool = False
    constructors: bool = True
    class_vars: bool = True
    instance_vars: bool = True
    inner_classes: bool = True
    methods: bool = True
    file_overview: bool = True
    public_only: bool = True
