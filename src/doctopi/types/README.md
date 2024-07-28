
types
=====

Contents
========

* [__init__](#__init__)
	* [Overview](#overview)
	* [Classes](#classes)
		* [AccessType](#accesstype)
		* [NameDescriptionType](#namedescriptiontype)
		* [Docstring](#docstring)
		* [FunctionDeclaration](#functiondeclaration)
		* [ClassDeclaration](#classdeclaration)
		* [DocFile](#docfile)
		* [DocDir](#docdir)
		* [Command](#command)
		* [MarkdownSettings](#markdownsettings)

# __init__

## Overview


Common types used by the doctopi package


## Classes

### AccessType


```python
class AccessType(Enum):
```

Enum of a class or function's access modifier
#### Class Variables

|Name|Type|Description|
| :--- | :--- | :--- |
|PUBLIC|None||
|PROTECTED|None||
|PRIVATE|None||

### NameDescriptionType


```python
@dataclass
class NameDescriptionType:
```

Data container for Name, Description, and Type used to describe
params, returns, members, etc.
#### Class Variables

|Name|Type|Description|
| :--- | :--- | :--- |
|name|str||
|description|str||
|type|str||

#### Methods

##### __post_init__


```python
def __post_init__(self):
```

Clean the input types of newlines
##### _strip_newlines


```python
def _strip_newlines(self, line: str) -> str:
```

Strip any newlines from a string

###### Args

|Name|Type|Description|
| :--- | :--- | :--- |
|line|str|any string|

###### Return

|Type|Description|
| :--- | :--- |
|str|provided string with newlines removed|

### Docstring


```python
@dataclass
class Docstring:
```

Doctopi representation of a docstring
#### Class Variables

|Name|Type|Description|
| :--- | :--- | :--- |
|summary|str||
|args|List[NameDescriptionType]||
|returns|NameDescriptionType||
|raises|List[NameDescriptionType]||

### FunctionDeclaration


```python
@dataclass
class FunctionDeclaration:
```

Doctopi representation of a function
#### Class Variables

|Name|Type|Description|
| :--- | :--- | :--- |
|name|str||
|signature|str||
|access|AccessType||
|docstring|Docstring||

### ClassDeclaration


```python
@dataclass
class ClassDeclaration:
```

Doctopi representation of a class
#### Class Variables

|Name|Type|Description|
| :--- | :--- | :--- |
|name|str||
|signature|str||
|docstring|Docstring||
|constructor|FunctionDeclaration||
|class_variables|List[NameDescriptionType]||
|member_variables|List[NameDescriptionType]||
|methods|List[FunctionDeclaration]||
|subclasses|List[ClassDeclaration]||

### DocFile


```python
@dataclass
class DocFile:
```

Doctopi representation of a source code file
#### Class Variables

|Name|Type|Description|
| :--- | :--- | :--- |
|name|str||
|path|Union[str, bytes, os.PathLike]||
|docstring|Docstring||
|classes|List[ClassDeclaration]||
|functions|List[FunctionDeclaration]||

### DocDir


```python
@dataclass
class DocDir:
```

Doctopi representation of a source code directory
#### Class Variables

|Name|Type|Description|
| :--- | :--- | :--- |
|name|str||
|path|Union[str, bytes, os.PathLike]||
|files|List[DocFile]||
|subdirs|List[DocDir]||

### Command


```python
class Command(ABC):
```

Generic class for the command design pattern
#### Methods

##### execute


```python
def execute(self):
```

Execute the command
### MarkdownSettings


```python
@dataclass
class MarkdownSettings:
```

Dataclass to hold Markdown content settings
#### Class Variables

|Name|Type|Description|
| :--- | :--- | :--- |
|src_language|str||
|table_align|str||
|table_of_contents|bool||
|constructors|bool||
|class_vars|bool||
|instance_vars|bool||
|inner_classes|bool||
|methods|bool||
|file_overview|bool||
|public_only|bool||
