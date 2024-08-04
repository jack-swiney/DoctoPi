"""This is an example python module"""
from __future__ import annotations
from enum import Enum

class ExampleGoogle:
    """This is an example of a class

    Attributes:
        likes_spam (bool): A boolean indicating if we like SPAM or not.
        eggs (int): An integer count of the eggs we have laid.
    """
    def __init__(self, likes_spam: bool = False, eggs: int = 0):
        """Constructor

        Args:
            likes_spam (bool, optional): A boolean indicating if we like
                SPAM or not. Defaults to False.
            eggs (int, optional): An integer count of the eggs we have
                laid. Defaults to 0.
        """
        self.likes_spam: bool = likes_spam
        self.eggs: int = eggs

    def example_foo(self, arg: int, arg2: str) -> bool:
        """Summary of example_foo

        Args:
            arg (int): description of arg
            arg2 (str): description of arg2

        Returns:
            bool: description of return value
        """
        return arg < 1 and not "no way" in arg2

    def example_bar(self, *args, **kwargs) -> bool:
        """Summary of example_bar

        Returns:
            bool: description of return value
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
        """Example of a class method

        Args:
            arg1 (int): description of arg1

        Raises:
            ValueError: arg1 in range [0,100]

        Returns:
            ExampleEnum: description of returns
        """
        if 0 > arg1 > 100:
            raise ValueError
        if arg1 > 90: return ExampleEnum.A
        elif arg1 > 80: return ExampleEnum.B
        elif arg1 > 70: return ExampleEnum.C
        elif arg1 > 60: return ExampleEnum.D
        return ExampleEnum.F


def example_function(arg1: int, arg2: ExampleEnum) -> int:
    """This is an example of a function, called example_function

    Args:
        arg1 (int): description of arg1
        arg2 (ExampleEnum): description of arg2

    Returns:
        int: The sum of arg1 and the value of arg2
    """
    return arg1 + arg2.value


class Outer:
    """Example of an outer class

    Attributes:
        value (int): the outer value
    """
    def __init__(self):
        self.value = 1

    class Inner:
        """Example of an inner class

        Attributes:
            value (int): the inner value
        """
        def __init__(self):
            self.value = -1

    def zero(self) -> int:
        """Return zero by exercising inner and outer classes

        Returns:
            int: zero
        """
        return self.value + self.Inner().value
