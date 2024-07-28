
cli
===

# \_\_init\_\_

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

### parse\_settings


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

### combine\_configs


```python
def combine_configs(default_config: configparser.ConfigParser, override_config: configparser.ConfigParser) -> configparser.ConfigParser:
```

Combine two config parsers, favoring the `override_config`

#### Args

|Name|Type|Description|
| :--- | :--- | :--- |
|default_config|configparser.ConfigParser|Config containing default values. Any args in the `override_config` will override these args.|
|override_config|configparser.ConfigParser|Config will be combined with the `default_config`, overriding any common arguments.|

#### Raises

|Type|Description|
| :--- | :--- |
|DoctoPiConfigError|If the `override_config` contains any sections or keys not in `default_config`.|

#### Return

|Type|Description|
| :--- | :--- |
|configparser.ConfigParser|_description_|

### ini\_to\_bool


```python
def ini_to_bool(ini_str: str) -> bool:
```

Convert ini value to python bool

#### Args

|Name|Type|Description|
| :--- | :--- | :--- |
|ini_str|str|value from ini|

#### Raises

|Type|Description|
| :--- | :--- |
|ValueError|provided value was not "yes" or "no"|

#### Return

|Type|Description|
| :--- | :--- |
|bool|yes or no|
