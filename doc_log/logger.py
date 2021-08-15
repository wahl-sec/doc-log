#!/usr/bin/env python3

from functools import wraps

from doc_log.parser import parse_docstring


def logger(logger="pep257"):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if func.__doc__:
                rules = parse_docstring(docstring=func.__doc__, logger=logger)
                print(rules)

            return func(*args, **kwargs)

        return wrapper

    return decorator
