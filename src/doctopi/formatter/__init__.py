"""TODO"""
# Built-in imports
from abc import ABC, abstractmethod

# Third-party imports

# This package imports


class Command(ABC):
    @abstractmethod
    def execute(self):
        pass
