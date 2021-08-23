#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import NoReturn, Tuple, List, Dict

import pytest

from doc_log.parser import parse_docstring
from doc_log.types import SectionItemTypeResult, type_check_arguments, type_check_rtypes


def _test_inner_types(_type: SectionItemTypeResult) -> NoReturn:
    """Assert that all nested items are correct in their types.

    :param _type: [description]
    :type _type: SectionItemTypeResult
    """
    assert _type.result and _type.expected == _type.actual
    for __type in _type._subitems:
        _test_inner_types(__type)


def test_type_check_pep257_style_nested_mixed_passive():
    def _test_func(i: Dict[str, int], j=0):
        """Function that returns two numbers in a weird format.

        Arguments:
        i -- the first number

        Types:
        j -- List[int]

        Keyword Arguments:
        j -- the second number (default 0)

        Returns:
        Result of addition between `i` and `j`.

        Return Type:
        Tuple[Tuple[int, int], int]
        """
        return ((i + j, i + j + 1), i)

    i, j = 2, 2
    parsed_docstring = parse_docstring(_test_func, dialect="pep257")
    type_check_results = type_check_arguments(
        parsed_docstring["types"],
        parameters={"i": {"first": i}, "j": [0, j]},
    )
    _test_inner_types(type_check_results["i"])
    _test_inner_types(type_check_results["j"])

    result = _test_func(i, j)
    type_check_returns = type_check_rtypes(parsed_docstring["rtypes"], results=[result])
    _test_inner_types(type_check_returns[0])
    assert result == ((4, 5), 2)


def test_type_check_epytext_style_nested_mixed_passive():
    def _test_func(i: Dict[str, int], j=0):
        """
        Function that adds two numbers and returns the result.

        @param i: the first number
        @param j: the second number
        @type j: List[int]
        @return: Result of addition between `i` and `j`.
        @rtype: Tuple[Tuple[int, int], int]
        """
        return ((i + j, i + j + 1), i)

    i, j = 2, 2
    parsed_docstring = parse_docstring(_test_func, dialect="epytext")
    type_check_results = type_check_arguments(
        parsed_docstring["types"],
        parameters={"i": {"first": i}, "j": [0, j]},
    )
    _test_inner_types(type_check_results["i"])
    _test_inner_types(type_check_results["j"])

    result = _test_func(i, j)
    type_check_returns = type_check_rtypes(parsed_docstring["rtypes"], results=[result])
    _test_inner_types(type_check_returns[0])
    assert result == ((4, 5), 2)


def test_type_check_rest_style_nested_mixed_passive():
    def _test_func(i: Dict[str, int], j=0):
        """Function that adds two numbers and returns the result.

        :param i: the first number
        :param j: the second number
        :type j: List[int]
        :return: Result of addition between `i` and `j`.
        :rtype: Tuple[Tuple[int, int], int]
        """
        return ((i + j, i + j + 1), i)

    i, j = 2, 2
    parsed_docstring = parse_docstring(_test_func, dialect="rest")
    type_check_results = type_check_arguments(
        parsed_docstring["types"],
        parameters={"i": {"first": i}, "j": [0, j]},
    )
    _test_inner_types(type_check_results["i"])
    _test_inner_types(type_check_results["j"])

    result = _test_func(i, j)
    type_check_returns = type_check_rtypes(parsed_docstring["rtypes"], results=[result])
    _test_inner_types(type_check_returns[0])
    assert result == ((4, 5), 2)


def test_type_check_google_style_nested_mixed_passive():
    def _test_func(i: Dict[str, int], j=0):
        """Function that adds two numbers and returns the result.

        Args:
            i: the first number
            j: the second number

        Types:
            j: List[int]

        Returns:
            Result of addition between `i` and `j`.

        Return Type:
            Tuple[Tuple[int, int], int]
        """
        return ((i + j, i + j + 1), i)

    i, j = 2, 2
    parsed_docstring = parse_docstring(_test_func, dialect="google")
    type_check_results = type_check_arguments(
        parsed_docstring["types"],
        parameters={"i": {"first": i}, "j": [0, j]},
    )
    _test_inner_types(type_check_results["i"])
    _test_inner_types(type_check_results["j"])

    result = _test_func(i, j)
    type_check_returns = type_check_rtypes(parsed_docstring["rtypes"], results=[result])
    _test_inner_types(type_check_returns[0])
    assert result == ((4, 5), 2)


def test_type_check_numpydoc_style_nested_mixed_passive():
    def _test_func(i: Dict[str, int], j=0):
        """Function that adds two numbers and returns the result.

        Parameters
        ----------
        i:
            the first number
        j:
            the second number

        Types
        -----
        j:
            List[int]

        Returns
        -------
            Result of addition between `i` and `j`.

        Return Type
        -----------
            Tuple[Tuple[int, int], int]
        """
        return ((i + j, i + j + 1), i)

    with pytest.raises(NotImplementedError):
        i, j = 2, 2
        parsed_docstring = parse_docstring(_test_func, dialect="numpydoc")
        type_check_results = type_check_arguments(
            parsed_docstring["types"],
            parameters={"i": {"first": i}, "j": [0, j]},
        )
        _test_inner_types(type_check_results["i"])
        _test_inner_types(type_check_results["j"])

        result = _test_func(i, j)
        type_check_returns = type_check_rtypes(
            parsed_docstring["rtypes"], results=[result]
        )
        _test_inner_types(type_check_returns[0])
        assert result == ((4, 5), 2)
