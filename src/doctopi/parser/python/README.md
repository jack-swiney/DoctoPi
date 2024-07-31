
python
======

Contents
========

* [docspec_adapter](#docspec_adapter)
	* [Overview](#overview)
	* [Classes](#classes)
		* [DocspecAdapter](#docspecadapter)
* [__init__](#__init__)
	* [Overview](#overview)

# docspec_adapter

## Overview


Adapter to convert docspec utilites/types to doctopi types. Used to
parse Python source code with Google, Numpy, EpyDoc, or Sphinx style
docstrings.


## Classes

### DocspecAdapter


```python
class DocspecAdapter(Parser):
```

Adapter to convert docspec utilites/types to doctopi types. Used to
parse Python source code with Google, Numpy, EpyDoc, or Sphinx style
docstrings.
#### Constructor


```python
DocspecAdapter(docstring_style: DocstringStyle):
```

Constructor

##### Args

|Name|Type|Description|
| :--- | :--- | :--- |
|docstring_style|docstring_parser.common.DocstringStyle|Use the DocstringStyle enum to toggle which type of docstring format to parse.|

#### Member Variables

|Name|Type|Description|
| :--- | :--- | :--- |
|docstring_style|docstring_parser.common.DocstringStyle|Use the DocstringStyle enum to toggle which type of docstring format to parse.|

#### Methods

##### parse_file


```python
def parse_file(self, file: Union[str, bytes, os.PathLike]) -> DocFile:
```

Parse a Python file and return a doctopi.DocFile object
representing the contents/docstrings.
###### Args

|Name|Type|Description|
| :--- | :--- | :--- |
|file|Union[str, bytes, os.PathLike]|File to parse|

###### Return

|Type|Description|
| :--- | :--- |
|DocFile|Representation of the file contents and docstrings|

##### parse_dir


```python
def parse_dir(self, root: Union[str, bytes, os.PathLike]) -> DocDir:
```

Walk a directory and parse the contents/docstrings of each
module
###### Args

|Name|Type|Description|
| :--- | :--- | :--- |
|root|Union[str, bytes, os.PathLike]|Source directory to walk and parse.|

###### Return

|Type|Description|
| :--- | :--- |
|DocDir|Collection of DocFile and DocDirs  mapping the provided directory to the doctopi documentation types.|

##### module_members


```python
def module_members(member_type: type, convert_func: Callable) -> Callable:
```

Decorator function for converting types from a dospec Module
into a list of doctopi types.
###### Args

|Name|Type|Description|
| :--- | :--- | :--- |
|member_type|type|type in docspec.Module.members to convert to doctopi type.|
|convert_func|Callable|function for converting the docspec module members of member_type to a doctopi type.|

###### Return

|Type|Description|
| :--- | :--- |
|Callable|Decorators return a Callable that wraps the function or class it decorates. See below for details on what is returned by the Callable itself.|

##### get_module_docstring


```python
def get_module_docstring(self, file: Union[str, bytes, os.PathLike]) -> Docstring:
```

Use the docspec adapter to parse a Python module and return
its docstring
###### Args

|Name|Type|Description|
| :--- | :--- | :--- |
|file|Union[str, bytes, os.PathLike]|Python module|

###### Return

|Type|Description|
| :--- | :--- |
|Docstring|Python module's docstring|

##### _get_module_docstring


```python
def _get_module_docstring(self, module: Module) -> Docstring:
```

Provided docspec has already parsed a module, use the adapter
to convert from docspec types to doctopi types, and return the
docstring of the module
###### Args

|Name|Type|Description|
| :--- | :--- | :--- |
|module|Module|Python module|

###### Return

|Type|Description|
| :--- | :--- |
|Docstring|Python module's docstring|

##### get_module_classes


```python
def get_module_classes(self, file: Union[str, bytes, os.PathLike]) -> List[ClassDeclaration]:
```

Use the docspec adapter to parse a Python module and return
its classes
###### Args

|Name|Type|Description|
| :--- | :--- | :--- |
|file|Union[str, bytes, os.PathLike]|Python module|

###### Return

|Type|Description|
| :--- | :--- |
|List[ClassDeclaration]|list of classes in the Python module|

##### _get_module_classes


```python
def _get_module_classes(self, module: Module) -> List[ClassDeclaration]:
```

Provided docspec has already parsed a module, use the adapter
to convert from docspec types to doctopi types, and return the
classes in the Python module
###### Args

|Name|Type|Description|
| :--- | :--- | :--- |
|module|Module|Python module|

###### Return

|Type|Description|
| :--- | :--- |
|List[ClassDeclaration]|list of classes in the Python module|

##### get_module_functions


```python
def get_module_functions(self, file: Union[str, bytes, os.PathLike]) -> List[FunctionDeclaration]:
```

Use the docspec adapter to parse a Python module and return
its functions
###### Args

|Name|Type|Description|
| :--- | :--- | :--- |
|file|Union[str, bytes, os.PathLike]|Python module|

###### Return

|Type|Description|
| :--- | :--- |
|List[FunctionDeclaration]|list of functions in the Python module|

##### _get_module_functions


```python
def _get_module_functions(self, module: Module) -> List[FunctionDeclaration]:
```

Provided docspec has already parsed a module, use the adapter
to convert from docspec types to doctopi types, and return the
functions in the Python module
###### Args

|Name|Type|Description|
| :--- | :--- | :--- |
|module|Module|Python module|

###### Return

|Type|Description|
| :--- | :--- |
|List[FunctionDeclaration]|list of functions in Python module|

##### _docspec_to_doctopi_docstring


```python
def _docspec_to_doctopi_docstring(self, docstring: docspec.Docstring) -> Docstring:
```

Convert a docspec.Docstring type into a doctopi.Docstring

###### Args

|Name|Type|Description|
| :--- | :--- | :--- |
|docstring|docspec.Docstring|docspec representation of a docstring|

###### Return

|Type|Description|
| :--- | :--- |
|Docstring|doctopi representation of a docstring|

##### _docspec_to_doctopi_function


```python
def _docspec_to_doctopi_function(self, function: Function) -> FunctionDeclaration:
```

Convert a docspec.Function type into a
doctopi.FunctionDeclaration
###### Args

|Name|Type|Description|
| :--- | :--- | :--- |
|function|Function|docspec representation of a function|

###### Return

|Type|Description|
| :--- | :--- |
|FunctionDeclaration|doctopi representation of a function|

##### _docspec_to_doctopi_class


```python
def _docspec_to_doctopi_class(self, cls: Class) -> ClassDeclaration:
```

convert a docspec.Class type into a doctopi.ClassDeclaration

###### Args

|Name|Type|Description|
| :--- | :--- | :--- |
|cls|Class|docspec representation of a class|

###### Return

|Type|Description|
| :--- | :--- |
|ClassDeclaration|doctopi representation of a class|

##### _parse_function_signature


```python
def _parse_function_signature(self, function: Function) -> str:
```

Take a docspec.Function object and put together the original
function's signature like it's written in the source code.
###### Args

|Name|Type|Description|
| :--- | :--- | :--- |
|function|Function|docspec representation of a Function|

###### Return

|Type|Description|
| :--- | :--- |
|str|function's signature|

##### _parse_class_signature


```python
def _parse_class_signature(self, cls: Class) -> str:
```

Take a docspec.Class object and put together the original
class's signature like it's written in the source code.
###### Args

|Name|Type|Description|
| :--- | :--- | :--- |
|cls|Class|docspec representation of a class|

###### Return

|Type|Description|
| :--- | :--- |
|str|class's signature|

##### _parse_access_type


```python
def _parse_access_type(self, function: Function) -> AccessType:
```

For Python, there's no real public, protected, or privates.
However, according to PEP8:
    _single_leading_underscore: weak “internal use” indicator.
        E.g. from M import * does not import objects whose names
        start with an underscore.
###### Args

|Name|Type|Description|
| :--- | :--- | :--- |
|function|Function|docspec representation of a function|

###### Return

|Type|Description|
| :--- | :--- |
|AccessType|Enum of public, private, or protected.|

# __init__

## Overview


Adapters to parse Python source code.

