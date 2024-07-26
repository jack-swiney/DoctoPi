"""Use the Factory Method design pattern to create a generic source code
parser."""
# Third-party imports
from docstring_parser.common import DocstringStyle

# This package imports
from doctopi.parser.python import DocspecAdapter
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
            "auto": DocspecAdapter(DocstringStyle.AUTO),
            "epydoc": DocspecAdapter(DocstringStyle.EPYDOC),
            "google": DocspecAdapter(DocstringStyle.GOOGLE),
            "numpy": DocspecAdapter(DocstringStyle.NUMPYDOC),
            "rest": DocspecAdapter(DocstringStyle.REST),
            "sphinx": DocspecAdapter(DocstringStyle.REST),
        }
    }

    try:
        return parsers[language][parser]
    except KeyError as exc:
        raise ValueError(f"No matching parser for language={language}, parser={parser}") from exc
