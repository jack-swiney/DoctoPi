
doctopi
=======

# \_\_init\_\_

# \_\_main\_\_

## Overview


DoctoPi main entrypoint


## Functions

### main


```python
def main(raw_args: List[str]):
```

Main method for DoctoPi

#### Args

|Name|Type|Description|
| :--- | :--- | :--- |
|raw_args|List[str]|System args|

#### Raises

|Type|Description|
| :--- | :--- |
|NotImplementedError|Running a command that isn't implemented|

### markdown


```python
def markdown(args: argparse.Namespace):
```

Build and execute a MarkdownBuilder

#### Args

|Name|Type|Description|
| :--- | :--- | :--- |
|args|argparse.Namespace|CLI arguments|

#### Raises

|Type|Description|
| :--- | :--- |
|DoctoPiConfigError|If a command from the ini doesn't exist|
