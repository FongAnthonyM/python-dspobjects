""" traces.py

"""
# Package Header #
from ...header import *

# Header #
__author__ = __author__
__credits__ = __credits__
__maintainer__ = __maintainer__
__email__ = __email__


# Imports #
# Standard Libraries #

# Third-Party Packages #
from baseobjects import BaseList

# Local Packages #


# Definitions #
# Classes #
class Traces(BaseList):
    """

    Class Attributes:

    Attributes:

    Args:

    """
    # Magic Methods #
    # Construction/Destruction
    def __init__(self, init: bool = True) -> None:
        # Parent Attributes #
        super().__init__(init=False)

        # New Attributes #
        self.parent = None

        self.groups = {}


        # Object Construction #
        if init:
            self.construct()

    # Instance Methods #
    # Constructors/Destructors
    def construct(self, ) -> None:
        pass

    def append(self, item):
        self.data.append(item)

    def insert(self, i, item):
        self.data.insert(i, item)

    def pop(self, i=-1):
        return self.data.pop(i)

    def remove(self, item):
        self.data.remove(item)

    def clear(self):
        self.data.clear()

    def copy(self):
        return self.__class__(self)

    def count(self, item):
        return self.data.count(item)

    def index(self, item, *args):
        return self.data.index(item, *args)

    def reverse(self):
        self.data.reverse()

    def sort(self, /, *args, **kwds):
        self.data.sort(*args, **kwds)

    def extend(self, other):
        if isinstance(other, UserList):
            self.data.extend(other.data)
        else:
            self.data.extend(other)