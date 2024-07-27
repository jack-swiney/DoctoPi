"""Common types used by the doctopi package"""
# Built-in imports
from __future__ import annotations
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
class ClassDeclaration:
    """Doctopi representation of a class"""
    name: str
    signature: str
    docstring: Docstring = None
    member_variables: List[NameDescriptionType] = field(default_factory=list)
    member_functions: List[FunctionDeclaration] = field(default_factory=list)
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
