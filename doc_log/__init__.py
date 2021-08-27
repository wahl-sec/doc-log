#!/usr/bin/env python3


from datetime import datetime
from inspect import FrameInfo, getmodule, stack
from functools import wraps
from typing import Optional
import logging

from doc_log.parser import parse_docstring, _get_context_frame
from doc_log.types import type_check_arguments, type_check_rtypes

logging.basicConfig(
    level=logging.INFO,
    encoding="utf-8",
    format="%(levelname)s :: %(asctime)s :: %(message)s",
)
LOGGER = logging.getLogger()


def doc_log(
    dialect: str,
    type_check: bool = True,
    _active_type_check: Optional[bool] = None,
):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if func.__doc__:
                rules = parse_docstring(_function=func, dialect=dialect)
                # TODO: Add validation checks for the rules to ensure expected format.

                _frame = _get_context_frame().frame
                if type_check:
                    if "types" in rules:
                        _type_check_arguments_results = type_check_arguments(
                            types=rules["types"],
                            arguments=args,
                            parameters=kwargs.copy(),  # A copy is necessary as this might be modified.
                        )

                        for (
                            parameter,
                            section_item_result,
                        ) in _type_check_arguments_results.items():
                            if not section_item_result.result:
                                if LOGGER.level >= logging.ERROR or _active_type_check:
                                    raise TypeError(
                                        "(doc-log :: {!s}:{!s}:{!s}) parameter: `{!s}` was not of expected type: `{!s}` was actually `{!s}`".format(
                                            _frame.f_code.co_name,
                                            func.__code__.co_firstlineno
                                            + 1
                                            + section_item_result.item.lineno,
                                            _frame.f_lineno,
                                            parameter,
                                            section_item_result.expected,
                                            section_item_result.actual,
                                        )
                                    )
                                else:
                                    LOGGER.warning(
                                        "(doc-log :: {!s}:{!s}:{!s}) parameter: `{!s}` was not of expected type: `{!s}` was actually `{!s}`".format(
                                            _frame.f_code.co_name,
                                            func.__code__.co_firstlineno
                                            + 1
                                            + section_item_result.item.lineno,
                                            _frame.f_lineno,
                                            parameter,
                                            section_item_result.expected,
                                            section_item_result.actual,
                                        )
                                    )
                    else:
                        LOGGER.warning(
                            "(doc-log :: {!s}:{!s}:{!s}) `type_check` was defined, however, no `types` section could be parsed.".format(
                                _frame.f_code.co_name,
                                func.__code__.co_firstlineno + 1,
                                _frame.f_lineno,
                            )
                        )

                    LOGGER.info(
                        "(doc-log :: {!s}:{!s}:{!s}) function: `{!s}` called from `{!s}` at: `{!s}`".format(
                            _frame.f_code.co_name,
                            func.__code__.co_firstlineno + 1,
                            _frame.f_lineno,
                            func.__name__,
                            getmodule(func).__file__,
                            datetime.now().isoformat(),
                        )
                    )
                    LOGGER.debug(
                        "(doc-log :: {!s}:{!s}:{!s}) function: `{!s}` was passed arguments: `{!r}` and keyword arguments: `{!r}`".format(
                            _frame.f_code.co_name,
                            func.__code__.co_firstlineno + 1,
                            _frame.f_lineno,
                            func.__name__,
                            args,
                            kwargs,
                        )
                    )
                _function_return_value = func(*args, **kwargs)

                _frame = _get_context_frame().frame
                if type_check:
                    if "rtypes" in rules:
                        _type_check_rtypes_result = type_check_rtypes(
                            rtypes=rules["rtypes"], results=_function_return_value
                        )

                        if not _type_check_rtypes_result.result:
                            if LOGGER.level >= logging.ERROR or _active_type_check:
                                raise TypeError(
                                    "(doc-log :: {!s}:{!s}:{!s}) return value was not of expected type: `{!s}` was actually `{!s}`".format(
                                        _frame.f_code.co_name,
                                        func.__code__.co_firstlineno
                                        + 1
                                        + _type_check_rtypes_result.item.lineno,
                                        _frame.f_lineno,
                                        _type_check_rtypes_result.expected,
                                        _type_check_rtypes_result.actual,
                                    )
                                )
                            else:
                                LOGGER.warning(
                                    "(doc-log :: {!s}:{!s}:{!s}) return value was not of expected type: `{!s}` was actually `{!s}`".format(
                                        _frame.f_code.co_name,
                                        func.__code__.co_firstlineno
                                        + 1
                                        + _type_check_rtypes_result.item.lineno,
                                        _frame.f_lineno,
                                        _type_check_rtypes_result.expected,
                                        _type_check_rtypes_result.actual,
                                    )
                                )
                    else:
                        LOGGER.warning(
                            "(doc-log :: {!s}:{!s}:{!s}) `type_check` was defined, however, no `rtypes` section could be parsed.".format(
                                _frame.f_code.co_name,
                                func.__code__.co_firstlineno + 1,
                                _frame.f_lineno,
                            )
                        )
            else:
                _function_return_value = func(*args, **kwargs)

            return _function_return_value

        return wrapper

    return decorator
