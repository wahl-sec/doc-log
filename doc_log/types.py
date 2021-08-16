#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import Dict, Any, List, Tuple

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
        raise KeyError("Provided section needs to be of type: 'types'")

    type_check_results = {parameter: None for parameter in parameters}
    for section_item in types.items:
        if section_item.name not in parameters:
            # TODO: Add some warning for if parameters provided and the ones
            # defined in 'types' section differ in either direction.
            continue

        _parameter_type = type(parameters[section_item.name]).__name__
        type_check_results[section_item.name] = SectionItemTypeResult(
            item=section_item,
            result=_parameter_type == section_item.value,
            expected=section_item.value,
            actual=_parameter_type,
        )

    return type_check_results


def type_check_rtypes(
    rtypes: Section, results: List[Any]
) -> Tuple[SectionItemTypeResult]:
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
        raise KeyError("Provided section needs to be of type: 'rtypes'")

    if len(rtypes.items) != len(results):
        # TODO: Add some warning for if parameters provided and the ones
        # defined in 'rtypes' section differ in either direction.
        pass

    type_check_results = tuple(type(_type).__name__ for _type in results)
    return tuple(
        SectionItemTypeResult(
            item=section_item,
            result=type_check_results[index] == section_item.value,
            expected=section_item.value,
            actual=type_check_results[index],
        )
        for index, section_item in enumerate(rtypes.items)
    )
