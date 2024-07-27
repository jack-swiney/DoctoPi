"""Use the Factory Method design pattern to create a generic source code
parser. Users of this package will immediately know "what's my
source code language", "where's my source code", and "what type of
docstring flavor am I using". The Factory Method design pattern will
allow users to instantiate the right kind of parsing adapter without
needing to see the details of the doctopi.parser package or any
configuration packages like docstring_parser.common.DocstringStyle.
"""

# Third-party imports
from docstring_parser.common import DocstringStyle

# This package imports
from doctopi.parser.python import DocspecAdapter
from doctopi.parser import Parser


# pylint: disable-next = invalid-name
def ParserFactory(language: str = "python", style: str = "google") -> Parser:
    """Factory Method to get a source code parser.

    Args:
        language (str, optional): programming language.
            Defaults to "python".
        style (str, optional): source code docstring style/flavor.
            Defaults to "google".

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
        return parsers[language][style]
    except KeyError as exc:
        raise ValueError(f"No matching parser for language={language}, style={style}") from exc
