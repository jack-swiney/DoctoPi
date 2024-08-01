"""Test doctopi.parser.python.docspec_adapter package"""
# Built-in imports
import os

# Third-party imports
import pytest

# This package imports
from doctopi.types import (AccessType, ClassDeclaration, DocFile, Docstring,
                           FunctionDeclaration, NameDescriptionType)
from doctopi.parser.parser_factory import ParserFactory


class TestDocspecAdapter:
    """Test doctopi.parser.python.docspec_adapter package"""

    @pytest.mark.parametrize("style", ["google", "rest", "numpy", "epydoc"])
    def test_parse_example_nominal(self, style: str):
        """Verify a module can be parsed"""
        # Get the path to the example python file
        path = os.path.join(os.path.dirname(__file__),
                            f"../examples/src/python/nominal/example_{style}.py")

        # Parse the file
        parser = ParserFactory("python", style)
        doc_file = parser.parse_file(path)

        # Verify the parsed DocFile matches the following:
        expected_doc_file = DocFile(
            name=f"example_{style}",
            path=os.path.normpath(path),
            docstring=Docstring(summary="This is an example python module"),
            classes=[
                ClassDeclaration(
                    name=f"Example{style.capitalize()}",
                    signature=f"class Example{style.capitalize()}:",
                    docstring=Docstring(
                        summary="This is an example of a class\n",
                        args=[
                            NameDescriptionType(
                                name="likes_spam",
                                type="bool",
                                description="A boolean indicating if we like SPAM or not."
                            ),
                            NameDescriptionType(
                                name="eggs",
                                type="int",
                                description="An integer count of the eggs we have laid."
                            )
                        ],
                        raises=[],
                        returns=None
                    ),
                    constructor=FunctionDeclaration(
                        name="__init__",
                        signature="def __init__(self, likes_spam: bool = False, eggs: int = 0):",
                        access=AccessType.PUBLIC,
                        docstring=Docstring(
                            # ReST/Sphinx doesn't do constructor docstrings
                            summary="Constructor\n" if not style=="rest" else "",
                            args=[
                                NameDescriptionType(
                                    name="likes_spam",
                                    description="A boolean indicating if we like SPAM or not. Defaults to False.",
                                    type="bool"
                                ),
                                NameDescriptionType(
                                    name="eggs",
                                    description="An integer count of the eggs we have laid. Defaults to 0.",
                                    type="int"
                                )
                            ] if not style =="rest" else [],
                            returns=None,
                            raises=[]
                        )
                    ),
                    class_variables=[],
                    member_variables=[
                        NameDescriptionType(
                            name="likes_spam",
                            description="A boolean indicating if we like SPAM or not.",
                            type="bool"
                        ),
                        NameDescriptionType(
                            name="eggs",
                            description="An integer count of the eggs we have laid.",
                            type="int"
                        )
                    ],
                    methods=[
                        FunctionDeclaration(
                            name="example_foo",
                            signature="def example_foo(self, arg: int, arg2: str) -> bool:",
                            access=AccessType.PUBLIC,
                            docstring=Docstring(
                                summary="Summary of example_foo\n",
                                args=[
                                    NameDescriptionType(
                                        name="arg",
                                        description="description of arg",
                                        type="int"
                                    ),
                                    NameDescriptionType(
                                        name="arg2",
                                        description="description of arg2",
                                        type="str"
                                    )
                                ],
                                raises=[],
                                returns=NameDescriptionType(
                                    name="",
                                    description="description of return value",
                                    type="bool"
                                )
                            )
                        ),
                        FunctionDeclaration(
                            name="example_bar",
                            signature="def example_bar(self, *args, **kwargs) -> bool:",
                            access=AccessType.PUBLIC,
                            docstring=Docstring(
                                summary="Summary of example_bar\n",
                                args=[],
                                raises=[],
                                returns=NameDescriptionType(
                                    name="",
                                    description="description of return value",
                                    type="bool"
                                )
                            )
                        )
                    ],
                    subclasses=[]
                ),
                ClassDeclaration(
                    name="ExampleEnum",
                    signature="class ExampleEnum(Enum):",
                    docstring=Docstring(
                        summary="Example of a class that inherits from another" ,
                        args=[],
                        raises=[],
                        returns=None
                    ),
                    constructor=None,
                    class_variables=[
                        NameDescriptionType(
                            name="A",
                            description="",
                            type=None
                        ),
                        NameDescriptionType(
                            name="B",
                            description="",
                            type=None
                        ),
                        NameDescriptionType(
                            name="C",
                            description="",
                            type=None
                        ),
                        NameDescriptionType(
                            name="D",
                            description="",
                            type=None
                        ),
                        NameDescriptionType(
                            name="F",
                            description="",
                            type=None
                        ),
                    ],
                    member_variables=[],
                    methods=[
                        FunctionDeclaration(
                            name="passing",
                            signature="def passing(cls, arg1: int) -> ExampleEnum:",
                            access=AccessType.PUBLIC,
                            docstring=Docstring(
                                summary="Example of a class method\n",
                                args=[
                                    NameDescriptionType(
                                        name="arg1",
                                        description="description of arg1",
                                        type="int"
                                    )
                                ],
                                returns=NameDescriptionType(
                                    name="",
                                    description="description of returns",
                                    type="ExampleEnum"
                                ),
                                raises=[
                                    NameDescriptionType(
                                        name="",
                                        description="arg1 in range [0,100]",
                                        type="ValueError"
                                    )
                                ]
                            )
                        )
                    ],
                    subclasses=[]
                ),
                ClassDeclaration(
                    class_variables=[],
                    constructor=FunctionDeclaration(
                        access=AccessType.PUBLIC,
                        docstring=Docstring(
                            args=[],
                            raises=[],
                            returns=None,
                            summary=''
                        ),
                        name='__init__',
                        signature='def __init__(self):'
                    ),
                    docstring=Docstring(
                        args=[
                            NameDescriptionType(
                                description='the outer value',
                                name='value',
                                type='int'
                            )
                        ],
                        raises=[],
                        returns=None,
                        summary='Example of an outer class\n'
                    ),
                    member_variables=[
                        NameDescriptionType(
                            description='the outer value',
                            name='value',
                            type='int'
                        )
                    ],
                    methods=[
                        FunctionDeclaration(
                            access=AccessType.PUBLIC,
                            docstring=Docstring(
                                args=[],
                                raises=[],
                                returns=NameDescriptionType(
                                    description='zero',
                                    name='',
                                    type='int'
                                ),
                                summary='Return zero by exercising inner and outer classes\n'
                            ),
                            name='zero',
                            signature='def zero(self) -> int:'
                        )
                    ],
                    name='Outer',
                    signature='class Outer:',
                    subclasses=[
                        ClassDeclaration(
                            class_variables=[],
                            constructor=FunctionDeclaration(
                                access=AccessType.PUBLIC,
                                docstring=Docstring(
                                    args=[],
                                    raises=[],
                                    returns=None,
                                    summary=''
                                ),
                                name='__init__',
                                signature='def __init__(self):'
                            ),
                            docstring=Docstring(
                                args=[
                                    NameDescriptionType(
                                        description='the inner value',
                                        name='value',
                                        type='int'
                                    )
                                ],
                                raises=[],
                                returns=None,
                                summary='Example of an inner class\n'
                            ),
                            member_variables=[
                                NameDescriptionType(
                                    description='the inner value',
                                    name='value',
                                    type='int'
                                )
                            ],
                            methods=[],
                            name='Inner',
                            signature='class Inner:',
                            subclasses=[]
                        )
                    ]
                )
            ],
            functions=[
                FunctionDeclaration(
                    name="example_function",
                    signature="def example_function(arg1: int, arg2: ExampleEnum) -> int:",
                    access=AccessType.PUBLIC,
                    docstring=Docstring(
                        summary="This is an example of a function, called example_function\n",
                        args=[
                            NameDescriptionType(
                                name="arg1",
                                description="description of arg1",
                                type="int"
                            ),
                            NameDescriptionType(
                                name="arg2",
                                description="description of arg2",
                                type="ExampleEnum"
                            )
                        ],
                        raises=[],
                        returns=NameDescriptionType(
                            description="The sum of arg1 and the value of arg2",
                            type="int"
                        )
                    )
                )
            ]
        )

        assert expected_doc_file == doc_file
