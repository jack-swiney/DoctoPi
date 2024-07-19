from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
import os
from typing import (List, Union)

class AccessType(Enum):
    PUBLIC = 1
    PROTECTED = 2
    PRIVATE = 3

@dataclass
class NameDescriptionTypePair:
    name: str = ""
    description: str = ""
    type: str = ""

@dataclass
class Docstring:
    summary: str = ""
    args: List[NameDescriptionTypePair] = []
    returns: NameDescriptionTypePair = None
    raises: List[NameDescriptionTypePair] = []

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
    member_variables: List[NameDescriptionTypePair] = []
    member_functions: List[FunctionDeclaration] = []
    subclasses: List[ClassDeclaration] = []

@dataclass
class DocFile:
    name: str
    path: Union[str, bytes, os.PathLike]
    docstring: Docstring = None
    classes: List[ClassDeclaration] = []
    functions: List[FunctionDeclaration] = []

@dataclass
class DocDir:
    name: str
    path: Union[str, bytes, os.PathLike]
    files: List[DocFile] = []
    subdirs: List[DocDir] = []
