
cli
===

Contents
========

* [__init__](#__init__)
	* [Overview](#overview)
	* [Classes](#classes)
		* [DoctoPiConfigError](#doctopiconfigerror)
	* [Functions](#functions)
		* [cli](#cli)
		* [parse_settings](#parse_settings)
		* [combine_configs](#combine_configs)
		* [ini_to_bool](#ini_to_bool)

# __init__

## Overview


Command-Line Interface (CLI). Defines the entrypoint for DoctoPi.


## Classes

### DoctoPiConfigError


```python
class DoctoPiConfigError(Exception):
```

Error occurred while configuration DoctoPi
## Functions

### cli


```python
def cli(sys_args: List[str]) -> argparse.Namespace:
```

Command-Line Interface (CLI)

#### Args

|Name|Type|Description|
| :--- | :--- | :--- |
|sys_args|List[str]|Arguments from the command line|

#### Return

|Type|Description|
| :--- | :--- |
|argparse.Namespace|Parsed arguments from CLI|

### parse_settings


```python
def parse_settings(cli_args: argparse.Namespace) -> argparse.Namespace:
```

Combine INI config settings with parsed arguments from CLI

#### Args

|Name|Type|Description|
| :--- | :--- | :--- |
|cli_args|argparse.Namespace|Parsed CLI arguments|

#### Return

|Type|Description|
| :--- | :--- |
|argparse.Namespace|Combined INI config and CLI arguments|

### combine_configs


```python
def combine_configs(default_config: configparser.ConfigParser, override_config: configparser.ConfigParser) -> configparser.ConfigParser:
```


### ini_to_bool


```python
def ini_to_bool(ini_str: str) -> bool:
```

Convert ini value to python bool

#### Args

|Name|Type|Description|
| :--- | :--- | :--- |
|ini_str|str|value from ini|

#### Raises

|Name|Type|Description|
| :--- | :--- | :--- |
||ValueError|provided value was not "yes" or "no"|

#### Return

|Type|Description|
| :--- | :--- |
|bool|yes or no|
