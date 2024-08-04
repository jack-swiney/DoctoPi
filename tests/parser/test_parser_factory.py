"""Tests for doctopi.parser.parser_factory module"""
# Third-party imports
from docstring_parser.common import DocstringStyle
import pytest

# This package imports
from doctopi.parser.parser_factory import ParserFactory
from doctopi.parser.python import DocspecAdapter


class TestParserFactory:

    @pytest.mark.parametrize("language", ["python"])
    @pytest.mark.parametrize("style,docstring_style", [
        ("auto", DocstringStyle.AUTO), ("epydoc", DocstringStyle.EPYDOC),
        ("google", DocstringStyle.GOOGLE), ("numpy", DocstringStyle.NUMPYDOC),
        ("rest", DocstringStyle.REST), ("sphinx", DocstringStyle.REST)
    ])
    def test_parser_factory_nominal(self, language, style, docstring_style):
        parser = ParserFactory(language=language, style=style)

        if language == "python":
            assert isinstance(parser, DocspecAdapter)
            assert parser.docstring_style == docstring_style

    @pytest.mark.parametrize("language,good_language", [
        ("python", True), ("Python", False), ("java", False), ("cpp", False), ("random", False)])
    @pytest.mark.parametrize("style,good_style", [
        ("auto", True), ("automatic", False), ("javadoc", False), ("doxygen", False), ("random", False)])
    def test_parser_factory_off_nominal(self, language, style, good_language, good_style):

        # Some overlap with params will test a nominal case, just skip those
        if good_language and good_style:
            return

        with pytest.raises(ValueError):
            ParserFactory(language=language, style=style)
