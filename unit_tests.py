def test_integers():
    """
    Check that a name with string integers still returns a dataset.
    """
    assert get_file("Wash23", "Ford2")

def test_large_page_number():
    """
    Check that a page number that exceeds the number of web pages
    returns an empty dataset.
    """
    assert get_file("George", "Washington", "2000000")