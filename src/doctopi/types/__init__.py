from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
import os
from typing import (List, Union)

class AccessType(Enum):
    PUBLIC = 1
    PROTECTED = 2
    PRIVATE = 3

@dataclass
class NameDescriptionType:
    name: str = ""
    description: str = ""
    type: str = ""

@dataclass
class Docstring:
    summary: str = ""
    args: List[NameDescriptionType] = field(default_factory=list)
    returns: NameDescriptionType = None
    raises: List[NameDescriptionType] = field(default_factory=list)

@dataclass
class FunctionDeclaration:
    name: str
    signature: str
    access: AccessType
    docstring: Docstring = None

@dataclass
class ClassDeclaration:
    name: str
    signature: str
    docstring: Docstring = None
    member_variables: List[NameDescriptionType] = field(default_factory=list)
    member_functions: List[FunctionDeclaration] = field(default_factory=list)
    subclasses: List[ClassDeclaration] = field(default_factory=list)

@dataclass
class DocFile:
    name: str
    path: Union[str, bytes, os.PathLike]
    docstring: Docstring = None
    classes: List[ClassDeclaration] = field(default_factory=list)
    functions: List[FunctionDeclaration] = field(default_factory=list)

@dataclass
class DocDir:
    name: str
    path: Union[str, bytes, os.PathLike]
    files: List[DocFile] = field(default_factory=list)
    subdirs: List[DocDir] = field(default_factory=list)
