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
                    if "types" in rules:
                        _type_check_arguments_results = type_check_arguments(
                            types=rules["types"], parameters=kwargs
                        )

                        for (
                            parameter,
                            section_item_result,
                        ) in _type_check_arguments_results.items():
                            if not section_item_result.result:
                                if active_type_check:
                                    raise TypeError(
                                        f"`{parameter}` was not of expected type: `{section_item_result.expected}` was actually `{section_item_result.actual}`"
                                    )
                                else:
                                    # TODO: Add logging warning for when item was not of expected type.
                                    pass

                    else:
                        # TODO: Add logging warning when parsed docstrings
                        # don't contain a `types` section.
                        pass

                    _function_return_value = func(*args, **kwargs)
                    if "rtypes" in rules:
                        _type_check_rtypes_results = type_check_rtypes(
                            rtypes=rules["rtypes"], results=[_function_return_value]
                        )

                        for rtype in _type_check_rtypes_results:
                            if not rtype.result:
                                if active_type_check:
                                    raise TypeError(
                                        f"return type was not of expected type: `{rtype.expected}` was actually `{rtype.actual}`"
                                    )
                                else:
                                    # TODO: Add logging warning for when item was not of expected type.
                                    pass

                    else:
                        # TODO: Add logging warning when parsed docstrings
                        # don't contain a `types` section.
                        pass

            else:
                _function_return_value = func(*args, **kwargs)

            return _function_return_value

        return wrapper

    return decorator
