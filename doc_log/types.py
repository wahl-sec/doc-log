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
    arguments: Section, parameters: Dict[str, Any], active_type_check: bool = False
) -> Dict[str, SectionItemTypeResult]:
    pass


def type_check_rtype(
    rtype: Section, result: List[Any], active_type_check: bool = False
) -> Tuple[SectionItemTypeResult]:
    pass
