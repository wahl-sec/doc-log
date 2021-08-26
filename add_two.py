# add_two.py

from doc_log.parser import parse_docstring


def add_two(i: int) -> int:
    """Add two (2) to a provided integer and return.

    Arguments:
    i -- the provided integer

    Returns:
    Integer `i` plus two (2)
    """
    return i + 2


print(parse_docstring(add_two, dialect="pep257"))
