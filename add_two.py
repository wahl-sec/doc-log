# add_two.py

from doc_log.parser import parse_docstring
from doc_log.types import type_check_arguments, type_check_rtypes


def add_two(i):
    """Add two (2) to a provided integer and return the original and the result.

    Arguments:
    i -- the provided integer

    Types:
    i -- Union[int, None]

    Returns:
    Integer `i` plus two (2)

    Return Type:
    Tuple[int, int]
    """
    return (i, i)


parameters = {"i": None}
result = add_two(**parameters)
docstring = parse_docstring(_function=add_two, dialect="pep257")

print("Arguments ==============")
print(type_check_arguments(docstring["types"], parameters=parameters))
print("Return ==============")
print(type_check_rtypes(docstring["rtypes"], results=result))
