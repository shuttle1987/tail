"""
Tests for the tail implementation
"""

from tail import FileBasedTail

def test_tail_from_file():
    """Tests that tail works as advertised from a file"""

    from unittest.mock import mock_open, patch, Mock

    # The mock_data we are using for our test
    mock_data = """A
B
C
D
E
F
"""
    mocked_open = mock_open(read_data=mock_data)

    # mock_open does not support iteration by lines by default so
    # we must define the following:
    mocked_open.return_value.__iter__.return_value = mock_data.splitlines()


    # The file check in the class returns no value upon a valid file
    # the error states just raise exceptions.
    mocked_file_validity_check = Mock()

    # We need to patch the open found in the namespace of the module
    # where the function is defined
    with patch('tail.open', mocked_open, create=True) as mocked_file_open:

        # We also need to patch the file checking because we are not dealing
        # with an actual file in the filesystem in this unit test
        with patch('tail.check_file_validity', mocked_file_validity_check):
            res = FileBasedTail('Test_filename.txt').tail(3)

    mocked_file_validity_check.assert_called_once_with('Test_filename.txt')
    mocked_file_open.assert_called_once_with('Test_filename.txt', 'r')
    assert len(res) == 3
    assert res == ["D", "E", "F"]
