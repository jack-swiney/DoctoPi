
parser
======

Contents
========

* [parser_factory](#parser_factory)
	* [Overview](#overview)
	* [Functions](#functions)
		* [ParserFactory](#parserfactory)
* [__init__](#__init__)
	* [Overview](#overview)
	* [Classes](#classes)
		* [Parser](#parser)

# parser_factory

## Overview


Use the Factory Method design pattern to create a generic source code
parser. Users of this package will immediately know "what's my
source code language", "where's my source code", and "what type of
docstring flavor am I using". The Factory Method design pattern will
allow users to instantiate the right kind of parsing adapter without
needing to see the details of the doctopi.parser package or any
configuration packages like docstring_parser.common.DocstringStyle.


## Functions

### ParserFactory


```python
def ParserFactory(language: str = "python", style: str = "google") -> Parser:
```

Factory Method to get a source code parser.

#### Args

|Name|Type|Description|
| :--- | :--- | :--- |
|language|str|programming language. Defaults to "python".|
|style|str|source code docstring style/flavor. Defaults to "google".|

#### Return

|Type|Description|
| :--- | :--- |
|Parser|Parser subclass specific to the provided language and parser type.|

# __init__

## Overview


The doctopi.parser package leverages the Adapter software design
pattern to adapt third-party tools and APIs for parsing source code
of varying languages, and converts them into doctopi types.


## Classes

### Parser


```python
class Parser(abc.ABC):
```

Generic source-code documentation parser. This is an abstract
base class and is intended to be extended for various programming
languages, and docstring flavors. The Parser will use the Adapter
software design pattern to adapt third-party tools and libraries
like Docspec, Doxygen, and Sphinx to a common documentation parser.
#### Methods

##### parse_file


```python
def parse_file(self, file: Union[str, bytes, os.PathLike]) -> DocFile:
```

To be overidden by the child classes (adapters). Takes a
source code file and parses it, returning the common doctopi
DocFile object.
###### Args

|Name|Type|Description|
| :--- | :--- | :--- |
|file|Union[str, bytes, os.PathLike]|File to parse.|

###### Return

|Type|Description|
| :--- | :--- |
|DocFile|Representation of the file contents and docstrings.|

##### parse_dir


```python
def parse_dir(self, root: Union[str, bytes, os.PathLike]) -> DocDir:
```

To be overidden by the child classes (adapters). Takes a
source code directory and recursively parses it, returning the
common doctopi DocDir object.
###### Args

|Name|Type|Description|
| :--- | :--- | :--- |
|root|Union[str, bytes, os.PathLike]|Source directory to walk and parse.|

###### Return

|Type|Description|
| :--- | :--- |
|DocDir|Collection of DocFile and DocDirs  mapping the provided directory to the doctopi documentation types.|
