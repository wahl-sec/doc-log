#!/usr/bin/env python3

from functools import wraps

from doc_log.parser import parse_docstring
from doc_log.types import type_check_arguments, type_check_rtypes


def doc_log(dialect: str, type_check: bool = True, active_type_check: bool = False):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if func.__doc__:
                rules = parse_docstring(docstring=func.__doc__, dialect=dialect)
                # TODO: Add validation checks for the rules to ensure expected format.

                if type_check:
                    pass

            return func(*args, **kwargs)

        return wrapper

    return decorator
