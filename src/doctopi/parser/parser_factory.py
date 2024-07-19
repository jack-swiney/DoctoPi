"""Use the Factory Method design pattern to create a generic source code
parser."""
from doctopi.parser.python import (EpydocAdapter, GoogleAdapter, NumpyAdapter, SphinxAdapter)
from doctopi.parser import Parser


def ParserFactory(language: str = "python", parser: str = "google") -> Parser:
    """Factory Method to get a source code parser.

    Args:
        language (str, optional): programming language.
            Defaults to "python".
        parser (str, optional): source code parser.
            Defaults to "sphinx".

    Returns:
        Parser: Parser subclass specific to the provided language and
        parser type.
    """

    parsers = {
        "cpp": {},
        "java": {},
        "python": {
            "epydoc": EpydocAdapter,
            "google": GoogleAdapter,
            "numpy": NumpyAdapter,
            "sphinx": SphinxAdapter
        }
    }

    try:
        return parsers[language][parser]()
    except KeyError as exc:
        raise ValueError(f"No matching parser for language={language}, parser={parser}") from exc
