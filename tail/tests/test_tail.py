"""
Tests for the tail implementation
"""

from tail import FileBasedTail

def test_tail_from_file():
    """Test that head works as advertised.
    we create a temporary file because mocking the tell method in mock.mock_open
    doesn't work without substantial extra effort
    """

    import tempfile
    with tempfile.NamedTemporaryFile(mode='w') as fp:
        fp.write("""A
B
C
D
E
F
""")
        fp.seek(0)
        tail_obj = FileBasedTail(fp.name)
        res = tail_obj.tail(3)
    assert len(res) == 3
    assert res == ["D", "E", "F"]


def test_head_from_real_file():
    """Test that head works as advertised.
    we create a temporary file because mocking the tell method in mock.mock_open
    doesn't work without substantial extra effort
    """

    import tempfile
    with tempfile.NamedTemporaryFile(mode='w') as fp:
        fp.write("""A
B
C
D
E
F
""")
        fp.seek(0)
        tail_obj = FileBasedTail(fp.name)
        res = tail_obj.head(3)
    assert len(res) == 3
    assert res == ["A", "B", "C"]

