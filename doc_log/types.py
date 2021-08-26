#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dataclasses import dataclass
from collections.abc import Iterable
from typing import Dict, Any, List, Tuple, Optional
import logging

LOGGER = logging.getLogger()

from doc_log.parser import Section, SectionItem


@dataclass
class SectionItemTypeResult:
    """Describes the results from type checking a given section item.
    Includes the expected type for the argument, the actual type provided
    at runtime and the conclusive result from type checking.
    """

    item: SectionItem
    result: bool
    expected: Any
    actual: Any
    _subitems: Optional[List["SectionItemTypeResult"]]

    def __str__(self: "SectionItemTypeResult") -> str:
        return "{!s} ({}): expected: ({!s}), actual: ({!s})".format(
            self.item, "OK" if self.result else "FAIL", self.expected, self.actual
        )


def _type_check_value(type_hint: str, value: Any, globals_: Dict[str, Any]) -> bool:
    """Type check a given value against a type hint. This check takes into account
    the different capitalizations of types and other special cases.

    :param type_hint: The type hint to check the value against.
    :type type_hint: str
    :param value: The value to type check.
    :type value: Any
    :param globals_: Additional custom types related to the local module.
    :type globals_: Dict[str, Any]
    :return: The result of the type checking.
    :rtype: bool
    """
    if type_hint == "AnyStr":
        return isinstance(value, (str, bytes))
    elif type_hint == "NoReturn":
        return value is None

    if type_hint in globals_:
        return globals_[type_hint] == type(value)

    return type_hint == type(value).__name__


def _type_check_nested_type(
    item: SectionItem, value: Any, globals_: Dict[str, Any]
) -> Tuple[SectionItemTypeResult, bool]:
    """Recursively check the nested type provided from the initial item.

    :param item: Nested item.
    :type item: SectionItem
    :param value: The value to compare type to.
    :type value: Any
    :param globals_: Additional custom types related to the local module.
    :type globals_: Dict[str, Any]
    :return: Tuple containing the result for each nested `SectionItem` and the result of type checking all items.
    :rtype: Tuple[SectionItem, bool]
    """
    item_type_result = SectionItemTypeResult(
        item=item,
        result=_type_check_value(item.value, value=value, globals_=globals_),
        expected=item.value,
        actual=type(value).__name__,
        _subitems=[],
    )

    if item.value in ("Union", "Optional"):
        if item.value == "Optional":
            item._subitems.append(
                SectionItem(value="NoneType", name=None, _subitems=[])
            )

        _result_flag = False
        for _item in item._subitems:
            _item_type_check = _type_check_nested_type(
                item=_item, value=value, globals_=globals_
            )
            _result_flag = _result_flag or _item_type_check.result
            item_type_result._subitems.append(_item_type_check)
        item_type_result.result = _result_flag
    else:
        if item._subitems:
            if isinstance(value, dict):
                LOGGER.debug(
                    "(doc-log) nested item was of type: `dict` with value: `{!s}`, type checking subitems: `{!s}`".format(
                        value, item._subitems
                    )
                )
                for _key in value.keys():
                    # TODO: Add check to see if item is iterable and of expected length.
                    _item_type_result = _type_check_nested_type(
                        item=item._subitems[0], value=_key, globals_=globals_
                    )
                    item_type_result._subitems.append(_item_type_result)
                    item_type_result.result = (
                        item_type_result.result
                        and _item_type_result.result == item_type_result.result
                    )

                for _value in value.values():
                    # TODO: Add check to see if item is iterable and of expected length.
                    _item_type_result = _type_check_nested_type(
                        item=item._subitems[1], value=_value, globals_=globals_
                    )
                    item_type_result._subitems.append(_item_type_result)
                    item_type_result.result = (
                        item_type_result.result
                        and _item_type_result.result == item_type_result.result
                    )
            elif isinstance(value, Iterable):
                LOGGER.debug(
                    "(doc-log) nested item was of type: `Iterable` with value: `{!s}`, type checking subitems: `{!s}`".format(
                        value, item._subitems
                    )
                )
                for index, _value in enumerate(value):
                    # TODO: Add check to see if item is iterable and of expected length.
                    if len(item._subitems) > 1:
                        _item_type_result = _type_check_nested_type(
                            item=item._subitems[index], value=_value, globals_=globals_
                        )
                    else:
                        _item_type_result = _type_check_nested_type(
                            item=item._subitems[0], value=_value, globals_=globals_
                        )

                    item_type_result._subitems.append(_item_type_result)
                    item_type_result.result = (
                        item_type_result.result
                        and _item_type_result.result == item_type_result.result
                    )

            else:
                LOGGER.debug(
                    "(doc-log) nested item was of non-container type with value: `{!s}`, type checking: `{!s}`".format(
                        value, item._subitems[0]
                    )
                )
                item_type_result._subitems.append(
                    SectionItemTypeResult(
                        item=item._subitems[0],
                        result=_type_check_value(
                            item._subitems[0].value, value=value, globals_=globals_
                        ),
                        expected=item._subitems[0].value,
                        actual=type(value).__name__,
                        _subitems=[],
                    )
                )
                item_type_result.result = (
                    item_type_result.result
                    and item._subitems[0].value == type(value).__name__
                )

    return item_type_result


def type_check_arguments(
    types: Section,
    parameters: Dict[str, Any] = {},
    arguments: Tuple[Any] = (),
    globals_: Optional[Dict[str, Any]] = globals(),
) -> Dict[str, SectionItemTypeResult]:
    """Check argument types for the given section to the actual types of the parameters.

    :param types: The parsed docstring section for `types`.
    :type types: Section
    :param parameters: The keyword arguments to be checked.
    :type parameters: Dict[str, Any], optional
    :param arguments: The arguments to be checked.
    :type arguments: Tuple[Any]
    :param globals_: Additional custom types related to the local module.
    :type globals_: Optional[Dict[str, Any]]
    :raises KeyError: If the `types` section is not provided as an argument.
    :return: The results for the parameter types.
    :rtype: Dict[str, SectionItemTypeResult]
    """
    if types.section != "types":
        raise KeyError("(doc-log) provided section needs to be of type: `types`")

    if arguments:
        for index, section_item in enumerate(
            [
                _section_item
                for _section_item in types.items
                if _section_item.name not in parameters
            ]
        ):
            if index >= len(arguments):
                break

            LOGGER.warning(
                "(doc-log) argument was passed as non-keyword guessing: `{!s} := {!r}`".format(
                    section_item.name, arguments[index]
                )
            )
            parameters[section_item.name] = arguments[index]

    _consumed = set()
    type_check_results = {
        parameter: SectionItemTypeResult(
            item=None, result=False, expected=Any, actual=None, _subitems=[]
        )
        for parameter in parameters
    }
    for section_item in types.items:
        if section_item.name not in parameters:
            # TODO: Don't warn if the parameter is optional.
            LOGGER.warning(
                "(doc-log) parameter: `{!s}` was type hinted, but not provided as a parameter.".format(
                    section_item.name
                )
            )
            continue

        _consumed.add(section_item.name)
        if section_item._subitems:
            LOGGER.debug(
                "(doc-log) item: `{!s}` is nested, type checking subitems".format(
                    section_item
                )
            )
            _section_item = _type_check_nested_type(
                section_item, value=parameters[section_item.name], globals_=globals_
            )
            type_check_results[section_item.name] = _section_item
        else:
            LOGGER.debug(
                "(doc-log) item: `{!s}` is not nested, type checking directly against value: `{!r}`".format(
                    section_item, parameters[section_item.name]
                )
            )
            _parameter_type = type(parameters[section_item.name]).__name__
            type_check_results[section_item.name] = SectionItemTypeResult(
                item=section_item,
                result=_type_check_value(
                    section_item.value, parameters[section_item.name], globals_=globals_
                ),
                expected=section_item.value,
                actual=_parameter_type,
                _subitems=[],
            )

    if len(_consumed) != len(parameters):
        LOGGER.warning(
            "(doc-log) parameters that were not type hinted was passed, consumed: `{!s}`, passed: `{!s}`".format(
                ", ".join(_consumed), ", ".join(parameters)
            )
        )

    # TODO: Log this in a better format.
    LOGGER.debug(
        "(doc-log) type check arguments results was: `{!r}`".format(type_check_results)
    )
    return type_check_results


def type_check_rtypes(
    rtypes: Section, results: Any, globals_: Optional[Dict[str, Any]] = globals()
) -> Tuple[SectionItemTypeResult]:
    """Check return types for the given section to the actual types of the output.

    :param rtypes: The parsed docstring section for `rtypes`.
    :type rtypes: Section
    :param results: The output values to be checked.
    :type results: List[Any]
    :param globals_: Additional custom types related to the local module.
    :type globals_: Optional[Dict[str, Any]]
    :raises KeyError: If the `rtypes` section is not provided as an argument.
    :return: The results for each return type.
    :rtype: Tuple[SectionItemTypeResult]
    """
    if rtypes.section != "rtypes":
        raise KeyError("Provided section needs to be of type: `rtypes`")

    type_check_results = SectionItemTypeResult(
        item=None, result=False, expected=Any, actual=None, _subitems=[]
    )

    for section_item in rtypes.items:
        if section_item._subitems:
            LOGGER.debug(
                "(doc-log) return type: `{!s}` is nested, type checking subitems".format(
                    section_item
                )
            )
            type_check_results = _type_check_nested_type(
                section_item, value=results, globals_=globals_
            )
        else:
            LOGGER.debug(
                "(doc-log) return type: `{!s}` is not nested, type checking directly against value: `{!r}`".format(
                    section_item, results
                )
            )
            _parameter_type = type(results).__name__
            type_check_results = SectionItemTypeResult(
                item=section_item,
                result=_type_check_value(
                    section_item.value, value=results, globals_=globals_
                ),
                expected=section_item.value,
                actual=_parameter_type,
                _subitems=[],
            )

    # TODO: Log this in a better format.
    LOGGER.debug(
        "(doc-log) type check return results was: `{!r}`".format(type_check_results)
    )
    return type_check_results
