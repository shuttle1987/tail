"""
This module provides a Python implementation of functionality of the GNU tail command.
"""

class TailBase:
    """
    Operations to extract the beginning or end of a stream
    """
    def __init__(self):
        raise NotImplementedError()

    def head(self, number_entries):
        """
        Retrieve the first number of entries from the stream
        :number_entries: how many items to retrieve
        """
        raise NotImplementedError()

    def tail(self, number_entries):
        """
        Retrieve the last number of entries from the stream
        :number_entries: how many items to retrieve
        """
        raise NotImplementedError()

class FileBasedTail(HeadTailBase):
    """Implement tail operations for a file object"""

    def __init__(self):
        raise NotImplementedError()

