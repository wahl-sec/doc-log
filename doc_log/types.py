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


def _type_check_nested_type(
    item: SectionItem, value: Any
) -> Tuple[SectionItemTypeResult, bool]:
    """Recursively check the nested type provided from the initial item.

    :param item: Nested item.
    :type item: SectionItem
    :param value: The value to compare type to.
    :type value: Any
    :return: Tuple containing the result for each nested `SectionItem` and the result of type checking all items.
    :rtype: Tuple[SectionItem, bool]
    """
    item_type_result, type_check_result = (
        SectionItemTypeResult(
            item=item,
            result=item.value == type(value).__name__,
            expected=item.value,
            actual=type(value).__name__,
            _subitems=[],
        ),
        item.value == type(value).__name__,
    )

    if item._subitems:
        if isinstance(value, dict):
            LOGGER.debug(
                "(doc-log) nested item was of type: `dict` with value: `{!s}`, type checking subitems: `{!s}`".format(
                    value, item._subitems
                )
            )
            for _key in value.keys():
                # TODO: Add check to see if item is iterable and of expected length.
                _item_type_result, _type_check_result = _type_check_nested_type(
                    item=item._subitems[0], value=_key
                )
                item_type_result._subitems.append(_item_type_result)
                type_check_result = (
                    type_check_result and _type_check_result == type_check_result
                )

            for _value in value.values():
                # TODO: Add check to see if item is iterable and of expected length.
                _item_type_result, _type_check_result = _type_check_nested_type(
                    item=item._subitems[1], value=_value
                )
                item_type_result._subitems.append(_item_type_result)
                type_check_result = (
                    type_check_result and _type_check_result == type_check_result
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
                    _item_type_result, _type_check_result = _type_check_nested_type(
                        item=item._subitems[index],
                        value=_value,
                    )
                else:
                    _item_type_result, _type_check_result = _type_check_nested_type(
                        item=item._subitems[0],
                        value=_value,
                    )

                item_type_result._subitems.append(_item_type_result)
                type_check_result = (
                    type_check_result and _type_check_result == type_check_result
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
                    result=item._subitems[0].value == type(value).__name__,
                    expected=item._subitems[0].value,
                    actual=type(value).__name__,
                    _subitems=[],
                )
            )
            type_check_result = (
                type_check_result and item._subitems[0].value == type(value).__name__
            )

    return item_type_result, type_check_result


def type_check_arguments(
    types: Section,
    parameters: Dict[str, Any],
) -> Dict[str, SectionItemTypeResult]:
    """Check argument types for the given section to the actual types of the parameters.

    :param types: The parsed docstring section for `types`.
    :type types: Section
    :param parameters: The parameters to be checked.
    :type parameters: Dict[str, Any]
    :raises KeyError: If the `types` section is not provided as an argument.
    :return: The results for the parameter types.
    :rtype: Dict[str, SectionItemTypeResult]
    """
    if types.section != "types":
        raise KeyError("provided section needs to be of type: `types`")

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
            _section_item, type_check_results_total = _type_check_nested_type(
                section_item, value=parameters[section_item.name]
            )
            type_check_results[section_item.name] = _section_item
            type_check_results[section_item.name].result = type_check_results_total
        else:
            LOGGER.debug(
                "(doc-log) item: `{!s}` is not nested, type checking directly against value: `{!r}`".format(
                    section_item, parameters[section_item.name]
                )
            )
            _parameter_type = type(parameters[section_item.name]).__name__
            type_check_results[section_item.name] = SectionItemTypeResult(
                item=section_item,
                result=_parameter_type == section_item.value,
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

    return type_check_results


def type_check_rtypes(rtypes: Section, results: Any) -> Tuple[SectionItemTypeResult]:
    """Check return types for the given section to the actual types of the output.

    :param rtypes: The parsed docstring section for `rtypes`.
    :type rtypes: Section
    :param results: The output values to be checked.
    :type results: List[Any]
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
            _section_item, type_check_results_total = _type_check_nested_type(
                section_item, value=results
            )

            _section_item.result = type_check_results_total
            type_check_results = _section_item
        else:
            LOGGER.debug(
                "(doc-log) return type: `{!s}` is not nested, type checking directly against value: `{!r}`".format(
                    section_item, results
                )
            )
            _parameter_type = type(results).__name__
            type_check_results = SectionItemTypeResult(
                item=section_item,
                result=_parameter_type == section_item.value,
                expected=section_item.value,
                actual=_parameter_type,
                _subitems=[],
            )

    return type_check_results
