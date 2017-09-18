"""
This module provides a Python implementation of functionality of the GNU tail command.
"""
class TailError(Exception):
    """Tail exceptions"""

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

class FileBasedTail(TailBase):
    """Implement tail operations for a file object"""

    def __init__(self, filename):
        """
        :filename: The name of the file to open
        """
        self.filename = filename
        check_file_validity(self.filename)

    def tail(self, number_lines=10):
        """
        :number_lines: the number of lines to take from the end of the file
        """
        raise NotImplementedError()


def check_file_validity(filename):
    """Check if a file exists is readable and is a vaild file"""
    raise NotImplementedError()


