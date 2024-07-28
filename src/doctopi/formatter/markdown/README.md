
markdown
========

# \_\_init\_\_

# markdown\_builder

## Overview


The MarkdownBuilder configures and generates documentation in
Markdown


## Classes

### MarkdownBuilder


```python
class MarkdownBuilder:
```

Build a Markdown formatter and generate documentation. Uses the
builder pattern to handle large amounts of configuration, and the
command pattern to allow users to customize/organize documentation.
#### Constructor


```python
MarkdownBuilder():
```

Constructor
#### Member Variables

|Name|Type|Description|
| :--- | :--- | :--- |
|src_language|str|Programming language of source code. Should be one of "python", "java", "cpp".|
|parser|Parser|DoctoPi source code parser.|
|src|Union[str, bytes, os.PathLike]|Source file/dir to parse.|
|output|Union[str, bytes, os.PathLike]|Markdown output file.|
|commands|List[Command]|List of markdon commands to execute using the Command pattern. These commands dictate how the markdown documentation should be organized.|
|recursive|bool|Toggle if the parser should stop at the root source directory provided or parse subdirectories. Default is False.|
|title|str|Title of the markdown document to create. Default is None.|
|author|str|Author of the markdown document to create. Default is None.|
|toc_depth|int|Heading depth of the table of contents. Value should be [1,6]. Default is 1.|
|toc_title|str|Title for the table of contents. Default is "Contents".|
|table_align|str|Text alignment for all markdown tables. Value should be one of "left", "center", or "right. Default is "left".|
|table_of_contents|bool|Toggle a table of contents to be generated. Default is False.|
|constructors|bool|Toggle constructors to be documented. Default is True.|
|class_vars|bool|Toggle class variables to be documented. Default is True.|
|instance_vars|bool|Toggle instance variables to be documented. Default is True.|
|inner_classes|bool|Toggle inner classes to be documented. Default is True.|
|methods|bool|Toggle member functions to be documented. Default is True.|
|file_overview|bool|Toggle file overview to be documented. Default is True.|
|public_only|bool|If enabled, only public class methods will be documented.|

#### Methods

##### build


```python
def build(self):
```

Generate the markdown by executing the provided commands
##### build\_dir


```python
def build_dir(self, md_utils: MdUtils, level: int, parsed_dir: DocDir):
```

Generate the markdown of a directory by executing the
provided commands
###### Args

|Name|Type|Description|
| :--- | :--- | :--- |
|md_utils|MdUtils|Markdown file generator|
|level|int|Starting heading level to build the provided file's documentation|
|parsed_dir|DocDir|parsed source directory|

##### build\_single\_file


```python
def build_single_file(self, md_utils: MdUtils, level: int, parsed_file: DocFile):
```

Generate the markdown of a single file by executing the
provided commands
###### Args

|Name|Type|Description|
| :--- | :--- | :--- |
|md_utils|MdUtils|Markdown file generator|
|level|int|Starting heading level to build the provided file's documentation|
|parsed_file|DocFile|parsed source file|

##### add\_file\_command


```python
def add_file_command(self, command: Type[Command]) -> MarkdownBuilder:
```

Add a Markdown generation command. Upon calling
MarkdownBuild.build(), commands will be executed one by one
to format and generate documentation in markdown.
###### Args

|Name|Type|Description|
| :--- | :--- | :--- |
|command|Type[Command]|Commands to execute at the file level|

###### Return

|Type|Description|
| :--- | :--- |
|MarkdownBuilder|This MarkdownBuilder|

##### add\_class\_commands


```python
def add_class_commands(self, command: Type[MarkdownClassAttrCommand]) -> MarkdownBuilder:
```

Add a Markdown generation command. Upon calling
MarkdownBuild.build(), commands will be executed one by one
to format and generate documentation in markdown.
###### Args

|Name|Type|Description|
| :--- | :--- | :--- |
|command|Type[Command]|Commands to execute at the class level|

###### Return

|Type|Description|
| :--- | :--- |
|MarkdownBuilder|This MarkdownBuilder|

##### add\_function\_commands


```python
def add_function_commands(self, command: Type[MarkdownDocstringCommand]) -> MarkdownBuilder:
```

Add a Markdown generation command. Upon calling
MarkdownBuild.build(), commands will be executed one by one
to format and generate documentation in markdown.
###### Args

|Name|Type|Description|
| :--- | :--- | :--- |
|command|Type[Command]|Commands to execute at the function level|

###### Return

|Type|Description|
| :--- | :--- |
|MarkdownBuilder|This MarkdownBuilder|

##### configure\_metadata


```python
def configure_metadata(self, title: str = "", author: str = "") -> MarkdownBuilder:
```

Configure Markdown file metadata

###### Args

|Name|Type|Description|
| :--- | :--- | :--- |
|title|str|Title of the markdown document to create. Defaults to "".|
|author|str|Author of the markdown document to create. Defaults to "".|

###### Return

|Type|Description|
| :--- | :--- |
|MarkdownBuilder|This MarkdownBuilder|

##### configure\_src


```python
def configure_src(self, language: str = "python", style: str = "google") -> MarkdownBuilder:
```

Configure the source progammming language and documentation
style
###### Args

|Name|Type|Description|
| :--- | :--- | :--- |
|language|str|programming language. Defaults to "python".|
|style|str|source code docstring style/flavor. Defaults to "google".|

###### Return

|Type|Description|
| :--- | :--- |
|MarkdownBuilder|This MarkdownBuilder object.|

##### configure\_io


```python
def configure_io(self, src: Union[str, bytes, os.PathLike], output: str = "README.md", recursive: bool = False) -> MarkdownBuilder:
```

Configure the Markdown builder to process a provided source
file or directory, recursive or not, and set the output markdown
file path/name.
###### Args

|Name|Type|Description|
| :--- | :--- | :--- |
|src|Union[str, bytes, os.PathLike]|Source file/dir to parse.|
|output|Union[str, bytes, os.PathLike]|Markdown output file. Defaults to "README.md".|
|recursive|bool|Toggle if the parser should stop at the root source directory provided or parse subdirectories.        Defaults to False.  Raises:|
|ValueError|None|If the src directory/file doesn't exist.|

###### Return

|Type|Description|
| :--- | :--- |
|MarkdownBuilder|This MarkdownBuilder object.|

##### enable\_toc


```python
def enable_toc(self, toc_depth: int = 1, title: str = "Contents") -> MarkdownBuilder:
```

Enable a table of contents for the generted markdown.
Configure the heading depth for the table and the title.
###### Args

|Name|Type|Description|
| :--- | :--- | :--- |
|toc_depth|int|Heading depth of the table of contents. Value should be [1,6]. Defaults to 1.|
|title|str|Title for the table of contents. Defaults to "Contents".|

###### Raises

|Type|Description|
| :--- | :--- |
|ValueError|If the toc_depth isn't between [1,6]|

###### Return

|Type|Description|
| :--- | :--- |
|MarkdownBuilder|This MarkdownBuilder.|

##### toggle


```python
def toggle(self, attr: str) -> MarkdownBuilder:
```

Toggle one of the many instance variables. See
MarkdownBuilder for list of all boolean variables to toggle. By
default, all are set to True except Table of Contents. To enable
the Table of contents, use MarkdownBuilder.enable_toc()
###### Args

|Name|Type|Description|
| :--- | :--- | :--- |
|attr|str|Instance variable in the MarkdownBuilder class|

###### Raises

|Type|Description|
| :--- | :--- |
|ValueError|If the provided attribute does exist but isn't a boolean.|
|AttributeError|If the provided attribute does not exist.|

###### Return

|Type|Description|
| :--- | :--- |
|MarkdownBuilder|This MarkdownBuilder|

##### align\_tables


```python
def align_tables(self, alignment: str) -> MarkdownBuilder:
```

Set text inside markdown tables to align left, center, or
right.
###### Args

|Name|Type|Description|
| :--- | :--- | :--- |
|alignment|str|Align text 'left', 'center', or 'right'.|

###### Raises

|Type|Description|
| :--- | :--- |
|ValueError|Invalid alignment string provided.|

###### Return

|Type|Description|
| :--- | :--- |
|MarkdownBuilder|This MarkdownBuilder|
