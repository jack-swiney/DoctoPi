
cmd
===

Contents
========

* [__init__](#__init__)
	* [Overview](#overview)
* [class_attr_commands](#class_attr_commands)
	* [Overview](#overview)
	* [Classes](#classes)
		* [MarkdownClassAttrCommand](#markdownclassattrcommand)
		* [MarkdownConstructorCommand](#markdownconstructorcommand)
		* [MarkdownClassVarCommand](#markdownclassvarcommand)
		* [MarkdownInstanceVarCommand](#markdowninstancevarcommand)
		* [MarkdownMethodsCommand](#markdownmethodscommand)
* [function_command](#function_command)
	* [Overview](#overview)
	* [Classes](#classes)
		* [MarkdownFunctionCommand](#markdownfunctioncommand)
* [param_table_command](#param_table_command)
	* [Overview](#overview)
	* [Classes](#classes)
		* [MarkdownParamTableCommand](#markdownparamtablecommand)
* [docstring_commands](#docstring_commands)
	* [Overview](#overview)
	* [Classes](#classes)
		* [MarkdownDocstringCommand](#markdowndocstringcommand)
		* [MarkdownArgsCommand](#markdownargscommand)
		* [MarkdownRaisesCommand](#markdownraisescommand)
		* [MarkdownReturnsCommand](#markdownreturnscommand)
* [class_command](#class_command)
	* [Overview](#overview)
	* [Classes](#classes)
		* [MarkdownClassCommand](#markdownclasscommand)
		* [MarkdownInnerClassCommand](#markdowninnerclasscommand)

# __init__

## Overview


Commands used by the MarkdownBuilder to generate markdown documentation


# class_attr_commands

## Overview


The Doctopi MarkdownBuilder class uses the Command design pattern to
let the user customize the documentation for various types. The
MarkdownClassAttrCommand class and child classes are used to document
various attributes of a class.


## Classes

### MarkdownClassAttrCommand


```python
class MarkdownClassAttrCommand(Command):
```

The MarkdownClassAttrCommand is used to define how to document
various attributes of a class, like inner classes, methods, etc.
#### Constructor


```python
MarkdownClassAttrCommand(md_utils: MdUtils, settings: MarkdownSettings, level: int, class_: ClassDeclaration, class_cmds: List[Type[MarkdownClassAttrCommand]], function_cmds: List[Type[MarkdownDocstringCommand]]):
```

Constructor

##### Args

|Name|Type|Description|
| :--- | :--- | :--- |
|md_utils|MdUtils|Markdown file generator|
|settings|MarkdownSettings|Markdown generator settings|
|level|int|Heading level to write the Class in markdown|
|class_|ClassDeclaration|The class to document|
|class_cmds|List[Type[MarkdownClassAttrCommand]]|List of commands to execute in order to document smaller pieces of the class, such as member variables, inner classes, methods, etc.|
|function_cmds|List[Type[MarkdownDocstringCommand]]|List of commands to execute in order to document smaller pieces of a function. This is needed by the constructor and method subcommands.|

##### Raises

|Name|Type|Description|
| :--- | :--- | :--- |
||ValueError|The heading level must be between [1,6]|

#### Member Variables

|Name|Type|Description|
| :--- | :--- | :--- |
|md_utils|MdUtils|Markdown file generator|
|settings|MarkdownSettings|Markdown generator settings|
|level|int|Heading level to write the Class in markdown|
|class_|ClassDeclaration|The class to document|
|class_cmds|List[Type[MarkdownClassAttrCommand]]|List of commands to execute in order to document smaller pieces of the class, such as member variables, inner classes, methods, etc.|
|function_cmds|List[Type[MarkdownDocstringCommand]]|List of commands to execute in order to document smaller pieces of a function. This is needed by the constructor and method subcommands.|

### MarkdownConstructorCommand


```python
class MarkdownConstructorCommand(MarkdownClassAttrCommand):
```

The MarkdownConstructorCommand is used to define how to document
a class constructor.
#### Member Variables

|Name|Type|Description|
| :--- | :--- | :--- |
|md_utils|MdUtils|Markdown file generator|
|level|int|Heading level to write the Class in markdown|
|class_|ClassDeclaration|The class to document|
|class_cmds|List[Type[MarkdownClassAttrCommand]]|List of commands to execute in order to document smaller pieces of the class, such as member variables, inner classes, methods, etc.|
|function_cmds|List[Type[MarkdownDocstringCommand]]|List of commands to execute in order to document smaller pieces of a function. This is needed by the constructor and method subcommands.|

#### Methods

##### execute


```python
def execute(self):
```

Add constructor documentation to the markdown generator
### MarkdownClassVarCommand


```python
class MarkdownClassVarCommand(MarkdownClassAttrCommand):
```

The MarkdownClassVarCommand is used to define how to document
class variables.
#### Member Variables

|Name|Type|Description|
| :--- | :--- | :--- |
|md_utils|MdUtils|Markdown file generator|
|level|int|Heading level to write the Class in markdown|
|class_|ClassDeclaration|The class to document|
|class_cmds|List[Type[MarkdownClassAttrCommand]]|List of commands to execute in order to document smaller pieces of the class, such as member variables, inner classes, methods, etc.|
|function_cmds|List[Type[MarkdownDocstringCommand]]|List of commands to execute in order to document smaller pieces of a function. This is needed by the constructor and method subcommands.|

#### Methods

##### execute


```python
def execute(self):
```

Add class variable documentation to the markdown generator
### MarkdownInstanceVarCommand


```python
class MarkdownInstanceVarCommand(MarkdownClassAttrCommand):
```

The MarkdownInstanceVarCommand is used to define how to document
instance variables.
#### Member Variables

|Name|Type|Description|
| :--- | :--- | :--- |
|md_utils|MdUtils|Markdown file generator|
|level|int|Heading level to write the Class in markdown|
|class_|ClassDeclaration|The class to document|
|class_cmds|List[Type[MarkdownClassAttrCommand]]|List of commands to execute in order to document smaller pieces of the class, such as member variables, inner classes, methods, etc.|
|function_cmds|List[Type[MarkdownDocstringCommand]]|List of commands to execute in order to document smaller pieces of a function. This is needed by the constructor and method subcommands.|

#### Methods

##### execute


```python
def execute(self):
```

Add instance variable documentation to the markdown generator
### MarkdownMethodsCommand


```python
class MarkdownMethodsCommand(MarkdownClassAttrCommand):
```

The MarkdownMethodsCommand is used to define how to
document class methods.
#### Member Variables

|Name|Type|Description|
| :--- | :--- | :--- |
|md_utils|MdUtils|Markdown file generator|
|level|int|Heading level to write the Class in markdown|
|class_|ClassDeclaration|The class to document|
|class_cmds|List[Type[MarkdownClassAttrCommand]]|List of commands to execute in order to document smaller pieces of the class, such as member variables, inner classes, methods, etc.|
|function_cmds|List[Type[MarkdownDocstringCommand]]|List of commands to execute in order to document smaller pieces of a function. This is needed by the constructor and method subcommands.|

#### Methods

##### execute


```python
def execute(self):
```

Add class method documentation to the markdown generator
# function_command

## Overview


The Doctopi MarkdownBuilder class uses the Command design pattern to
let the user customize the documentation for various types. The
MarkdownFunctionCommand is used to define how to document a function.


## Classes

### MarkdownFunctionCommand


```python
class MarkdownFunctionCommand(Command):
```

The MarkdownFunctionCommand is used to define how to document a
function. It uses various sub-commands to document params, returns,
exceptions, etc.
#### Constructor


```python
MarkdownFunctionCommand(md_utils: MdUtils, settings: MarkdownSettings, level: int, func: FunctionDeclaration, cmds: List[Type[MarkdownDocstringCommand]]):
```


#### Member Variables

|Name|Type|Description|
| :--- | :--- | :--- |
|md_utils|MdUtils|Markdown file generator|
|settings|MarkdownSettings|Markdown generator settings|
|level|int|Heading level to write the Class in markdown|
|func|FunctionDelcaration|The function to document|
|cmds|List[MarkdownDocstringCommand]|List of commands to execute in order to document params, returns, and exceptions|

#### Methods

##### execute


```python
def execute(self):
```

Add function documentation to the markdown generator
# param_table_command

## Overview


The MarkdownParamTableCommand configures a markdown table and
adds it to a markdown generator.


## Classes

### MarkdownParamTableCommand


```python
class MarkdownParamTableCommand(Command):
```

The MarkdownParamTableCommand is used to define how to document a
table of parameters. A param table will have columns for Name, Type,
and Description.
#### Constructor


```python
MarkdownParamTableCommand(md_utils: MdUtils, settings: MarkdownSettings, table_rows: List[NameDescriptionType]):
```


#### Member Variables

|Name|Type|Description|
| :--- | :--- | :--- |
|md_utils|MdUtils|Markdown file generator|
|settings|MarkdownSettings|Markdown generator settings|
|table_rows|List[NameDescriptionType]|Table contents|

#### Methods

##### execute


```python
def execute(self):
```

Add param table to the markdown generator
# docstring_commands

## Overview


The Doctopi MarkdownBuilder class uses the Command design pattern to
let the user customize the documentation for various types. The
MarkdownDocstringCommand is used to define how to document the params,
exceptions, and returns of a function.


## Classes

### MarkdownDocstringCommand


```python
class MarkdownDocstringCommand(Command):
```

Generic class for markdown commands specific to docstring params

#### Constructor


```python
MarkdownDocstringCommand(md_utils: MdUtils, settings: MarkdownSettings, level: int, docstring: Docstring):
```


#### Member Variables

|Name|Type|Description|
| :--- | :--- | :--- |
|md_utils|MdUtils|Markdown file generator|
|settings|MarkdownSettings|Markdown generator settings|
|level|int|Heading level to write the Class in markdown|
|docstring|Docstring]|docstring to document|

### MarkdownArgsCommand


```python
class MarkdownArgsCommand(MarkdownDocstringCommand):
```

The MarkdownArgsCommand is used to define how to document
function arguments from a docstring into markdown.
#### Member Variables

|Name|Type|Description|
| :--- | :--- | :--- |
|md_utils|MdUtils|Markdown file generator|
|level|int|Heading level to write the Class in markdown|
|params|List[NameDescriptionType]|Table contents|

#### Methods

##### execute


```python
def execute(self):
```

Add function argument documentation to the markdown generator
### MarkdownRaisesCommand


```python
class MarkdownRaisesCommand(MarkdownDocstringCommand):
```

The MarkdownRaisesCommand is used to define how to document
exceptions a function raises from a docstring into markdown.
#### Member Variables

|Name|Type|Description|
| :--- | :--- | :--- |
|md_utils|MdUtils|Markdown file generator|
|level|int|Heading level to write the Class in markdown|
|params|List[NameDescriptionType]|Table contents|

#### Methods

##### execute


```python
def execute(self):
```

Add function exception documentation to the markdown
generator
### MarkdownReturnsCommand


```python
class MarkdownReturnsCommand(MarkdownDocstringCommand):
```

The MarkdownReturnsCommand is used to define how to document
a function's return type from a docstring into markdown.
#### Member Variables

|Name|Type|Description|
| :--- | :--- | :--- |
|md_utils|MdUtils|Markdown file generator|
|level|int|Heading level to write the Class in markdown|
|params|List[NameDescriptionType]|Table contents|

#### Methods

##### execute


```python
def execute(self):
```

Add function returns documentation to the markdown generator
# class_command

## Overview


The Doctopi MarkdownBuilder class uses the Command design pattern to
let the user customize the documentation for various types. The
MarkdownClassCommand is used to define how to document a class. It uses
various sub-commands to recursively document inner classes, methods,
etc.


## Classes

### MarkdownClassCommand


```python
class MarkdownClassCommand(MarkdownClassAttrCommand):
```

The MarkdownClassCommand is used to define how to document a
class. It uses various sub-commands to recursively document inner
classes, methods, etc.
#### Member Variables

|Name|Type|Description|
| :--- | :--- | :--- |
|md_utils|MdUtils|Markdown file generator|
|level|int|Heading level to write the Class in markdown|
|class_|ClassDeclaration|The class to document|
|class_cmds|List[MarkdownClassAttrCommand]|List of commands to execute in order to document smaller pieces of the class, such as member variables, inner classes, methods, etc.|
|function_cmds|List[MarkdownDocstringCommand]|List of commands to execute in order to document smaller pieces of a function. This is needed by the constructor and method subcommands.|

#### Methods

##### execute


```python
def execute(self):
```

Add class documentation to the markdown generator
### MarkdownInnerClassCommand


```python
class MarkdownInnerClassCommand(MarkdownClassAttrCommand):
```

The MarkdownInnerClassCommand is used to define how to document
an inner class. It uses various sub-commands to recursively document
additional inner classes, methods, etc.
#### Member Variables

|Name|Type|Description|
| :--- | :--- | :--- |
|md_utils|MdUtils|Markdown file generator|
|level|int|Heading level to write the Class in markdown|
|class_|ClassDeclaration|The class to document|
|class_cmds|List[MarkdownClassAttrCommand]|List of commands to execute in order to document smaller pieces of the class, such as member variables, inner classes, methods, etc.|
|function_cmds|List[MarkdownDocstringCommand]|List of commands to execute in order to document smaller pieces of a function. This is needed by the constructor and method subcommands.|

#### Methods

##### execute


```python
def execute(self):
```

Add inner class documentation to the markdown generator