"""This is an example python module"""
from __future__ import annotations
from enum import Enum

class ExampleEpydoc:
    """
    This is an example of a class

    @param likes_spam: A boolean indicating if we like SPAM or not.
    @type likes_spam: bool
    @param eggs: An integer count of the eggs we have laid.
    @type eggs: int
    """

    def __init__(self, likes_spam: bool = False, eggs: int = 0):
        """
        Constructor

        @param likes_spam: A boolean indicating if we like SPAM or not.
            Defaults to False.
        @type likes_spam: bool
        @param eggs: An integer count of the eggs we have laid. Defaults
            to 0.
        @type eggs: int
        """
        self.likes_spam: bool = likes_spam
        self.eggs: int = eggs

    def example_foo(self, arg: int, arg2: str) -> bool:
        """
        Summary of example_foo

        @param arg: description of arg
        @type arg: int
        @param arg2: description of arg2
        @type arg2: str
        @return: description of return value
        @rtype: bool
        """
        return arg < 1 and not "no way" in arg2

    def example_bar(self, *args, **kwargs) -> bool:
        """
        Summary of example_bar

        @return: description of return value
        @rtype: bool
        """
        return len(args) > 0 or "my_kwarg" in kwargs


class ExampleEnum(Enum):
    """Example of a class that inherits from another"""

    A = 1
    B = 2
    C = 3
    D = 4
    F = 6

    @classmethod
    def passing(cls, arg1: int) -> ExampleEnum:
        """
        Example of a class method

        @param arg1: description of arg1
        @type arg1: int
        @raise ValueError: arg1 in range [0,100]
        @return: description of returns
        @rtype: ExampleEnum
        """
        if 0 > arg1 > 100:
            raise ValueError
        if arg1 > 90: return ExampleEnum.A
        elif arg1 > 80: return ExampleEnum.B
        elif arg1 > 70: return ExampleEnum.C
        elif arg1 > 60: return ExampleEnum.D
        return ExampleEnum.F


def example_function(arg1: int, arg2: ExampleEnum) -> int:
    """
    This is an example of a function, called example_function

    @param arg1: description of arg1
    @type arg1: int
    @param arg2: description of arg2
    @type arg2: ExampleEnum
    @return: The sum of arg1 and the value of arg2
    @rtype: int
    """
    return arg1 + arg2.value


class Outer:
    """
    Example of an outer class

    @param value: the outer value
    @type value: int
    """

    def __init__(self):
        self.value = 1

    class Inner:
        """
        Example of an inner class

        @param value: the inner value
        @type value: int
        """

        def __init__(self):
            self.value = -1

    def zero(self) -> int:
        """
        Return zero by exercising inner and outer classes

        @return: zero
        @rtype: int
        """
        return self.value + self.Inner().value
