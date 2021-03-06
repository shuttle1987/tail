"""
This module provides a Python implementation of functionality of the GNU tail command.
"""
import os

class TailError(Exception):
    """Tail exceptions"""

class TailBase:
    """
    Operations to extract the beginning or end of a stream
    """
    line_terminators = ('\r\n', '\n', '\r')

    def __init__(self, initial_position, read_buffer_size=None):
        """
        We have to keep track of the current position we are at.
        :read_buffer_size: how many items to read ahead when searching for separators,
                           if not given read until the end.
        """
        self.position_index = initial_position
        self.read_size = read_buffer_size

    def head(self, number_entries):
        """
        Retrieve the first number of entries from the stream
        :number_entries: how many items to retrieve
        """
        raise NotImplementedError()

    def tail(self, number_entries=10):
        """
        Retrieve the last number of entries from the stream
        :number_entries: how many items to retrieve
        """
        raise NotImplementedError()

    def seek_line_backwards(self):
        """
        Searches backwards from the current position for a line terminator
        and seeks to the position of character immediately after it.
        :returns: Returns the position immediately after the line separator or None if not found.
        """
        pos = end_pos = self.current_position()

        read_size = self.read_size
        if pos > read_size:
            pos -= read_size
        else:
            pos = 0
            read_size = end_pos

        self.seek(pos)

        bytes_read, read_str = self.read(read_size)

        if bytes_read and read_str[-1] in self.line_terminators:
            # The last charachter is a line terminator, don't count this one
            bytes_read -= 1

            if read_str[-2:] == '\r\n' and '\r\n' in self.line_terminators:
                # found crlf
                bytes_read -= 1

        while bytes_read > 0:
            # Scan backwards, counting the newlines in the current buffer
            i = bytes_read - 1
            while i >= 0:
                if read_str[i] in self.line_terminators:
                    self.seek(pos + i + 1)
                    return self.current_position()
                i -= 1

            if pos == 0 or pos - self.read_size < 0:
                # Not enought lines in the buffer, send the whole file
                self.seek(0)
                return None

            pos -= self.read_size
            self.seek(pos)

            bytes_read, read_str = self.read(self.read_size)

        return None

    def seek(self, position):
        """Seek in the underlying data, specalizations to be implemented by derived classes"""
        self.position_index = position


    def seek_line_forward(self):
        """
        Searches forward from the current file position for a line separator
        and seeks to the position of character immediately after it.
        :returns: Returns the position immediately after the line separator or None if not found.
        """
        pos = self.current_position()

        bytes_read, read_str = self.read(self.read_size)

        start = 0
        if bytes_read and read_str[0] in self.line_terminators:
            # If the first character is a line terminator skip over it
            start += 1

        while bytes_read > 0:
            # Now we scan forwards,for line terminators in the current buffer
            i = start
            while i < bytes_read:
                if read_str[i] in self.line_terminators:
                    self.seek(pos + i + 1)
                    return self.current_position()
                i += 1

            pos += self.read_size
            self.seek(pos)

            bytes_read, read_str = self.read(self.read_size)

        return None


    def read(self, read_size=None):
        """Read from the stream.
        :read_size: number of items to read from the current position onwards, if no parameter
                    is given the default is to read everything from the current position onwards.
        :returns: A tuple of the length of the data and the data
        """
        raise NotImplementedError()

    def current_position(self):
        """Return the current index in the stream
        """
        return self.position_index


class FileBasedTail(TailBase):
    """Implement tail operations for a file object"""

    def __init__(self, filename, read_buffer_size=1024):
        """
        :filename: The name of the file to open
        :read_buffer_size: How many bytes to read ahead
        """
        self.filename = filename
        check_file_validity(self.filename)
        self.file_obj = open(filename, 'r')
        super().__init__(initial_position=0, read_buffer_size=read_buffer_size)

    def head(self, lines=10):
        """
        Return the top lines of the file.
        :lines: maximum number of lines to extract
        """
        self.seek(0)

        for _ in range(lines):
            if not self.seek_line_forward():
                break

        end_pos = self.current_position()

        self.seek(0)
        _, data = self.read(end_pos - 1)

        if data:
            return data.splitlines()
        return []

    def tail(self, lines=10):
        """
        Get the last number of lines from a file
        :lines: the number of lines to take from the end of the file
        """
        self.seek_to_end()
        end_pos = self.current_position()

        for _ in range(lines):
            if not self.seek_line_backwards():
                break

        _, data = self.read(end_pos - self.current_position() - 1)
        if data:
            return data.splitlines()
        return []

    def seek(self, position, whence=0):
        """
        Seek to position relative to place specified by whence
        :position: where to move the filepointer to
        :whence: which relative position to use, same as Python's file objects.
                 0 is beginning of file, 1 is the current position, 2 is end of file position.
        """
        self.file_obj.seek(position, whence)
        self.position_index = self.file_obj.tell()

    def seek_to_end(self):
        """Seek to the end of the file"""
        self.seek(0, 2)


    def read(self, read_size=None):
        """Read the next read_size bytes from the current file position or all of
        the rest of the file if not specified.
        """
        if read_size:
            data = self.file_obj.read(read_size)
        else:
            data = self.file_obj.read()
        return len(data), data

    def current_position(self):
        """Return the current position in the file that the file pointer is pointed at"""
        self.position_index = self.file_obj.tell()
        return self.position_index


def check_file_validity(filename):
    """Check if a file exists is readable and is a vaild file"""
    if not os.access(filename, os.F_OK):
        raise TailError("File '{}' does not exist".format(filename))
    if not os.access(filename, os.R_OK):
        raise TailError("File '{}' is not readable".format(filename))
    if os.path.isdir(filename):
        raise TailError("'{}' is a directory and not a file".format(filename))
