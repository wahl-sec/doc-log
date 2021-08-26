#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import NoReturn, Tuple, List, Dict

import pytest

from doc_log.parser import parse_docstring
from doc_log.types import SectionItemTypeResult, type_check_arguments, type_check_rtypes


def test_type_check_pep257_style_nested_invalid_mixed_passive():
    def _test_func(i: Dict[str, int], j: List[int] = 0) -> Tuple[Tuple[int, int], int]:
        """Function that returns two numbers in a weird format.

        Arguments:
        i -- the first number

        Types:
        i -- Dict[str, str]
        j -- List[str]

        Keyword Arguments:
        j -- the second number (default 0)

        Returns:
        Result of addition between `i` and `j`.

        Return Type:
        Tuple[Tuple[str, str], str]
        """
        return ((i + j, i + j + 1), i)

    i, j = 2, 2
    parsed_docstring = parse_docstring(_test_func, dialect="pep257")
    type_check_results = type_check_arguments(
        parsed_docstring["types"],
        parameters={"i": {"first": i}, "j": [0, j]},
    )
    assert not type_check_results["i"].result
    assert list(
        (item.result, item.expected, item.actual)
        for item in type_check_results["i"]._subitems
    ) == [(True, "str", "str"), (False, "str", "int")]

    assert not type_check_results["j"].result
    assert list(
        (item.result, item.expected, item.actual)
        for item in type_check_results["j"]._subitems
    ) == [(False, "str", "int"), (False, "str", "int")]

    result = _test_func(i, j)
    type_check_returns = type_check_rtypes(parsed_docstring["rtypes"], results=result)
    assert not type_check_returns.result
    assert list(
        (item.result, item.expected, item.actual)
        for item in type_check_returns._subitems
    ) == [(False, "tuple", "tuple"), (False, "str", "int")]
    assert list(
        (item.result, item.expected, item.actual)
        for item in type_check_returns._subitems[0]._subitems
    ) == [(False, "str", "int"), (False, "str", "int")]

    assert result == ((4, 5), 2)


def test_type_check_epytext_style_nested_invalid_mixed_passive():
    def _test_func(i: Dict[str, int], j: List[int] = 0) -> Tuple[Tuple[int, int], int]:
        """
        Function that adds two numbers and returns the result.

        @param i: the first number
        @type i: Dict[str, str]
        @param j: the second number
        @type j: List[str]
        @return: Result of addition between `i` and `j`.
        @rtype: Tuple[Tuple[str, str], str]
        """
        return ((i + j, i + j + 1), i)

    i, j = 2, 2
    parsed_docstring = parse_docstring(_test_func, dialect="epytext")
    type_check_results = type_check_arguments(
        parsed_docstring["types"],
        parameters={"i": {"first": i}, "j": [0, j]},
    )
    assert not type_check_results["i"].result
    assert list(
        (item.result, item.expected, item.actual)
        for item in type_check_results["i"]._subitems
    ) == [(True, "str", "str"), (False, "str", "int")]

    assert not type_check_results["j"].result
    assert list(
        (item.result, item.expected, item.actual)
        for item in type_check_results["j"]._subitems
    ) == [(False, "str", "int"), (False, "str", "int")]

    result = _test_func(i, j)
    type_check_returns = type_check_rtypes(parsed_docstring["rtypes"], results=result)
    assert not type_check_returns.result
    assert list(
        (item.result, item.expected, item.actual)
        for item in type_check_returns._subitems
    ) == [(False, "tuple", "tuple"), (False, "str", "int")]
    assert list(
        (item.result, item.expected, item.actual)
        for item in type_check_returns._subitems[0]._subitems
    ) == [(False, "str", "int"), (False, "str", "int")]

    assert result == ((4, 5), 2)


def test_type_check_rest_style_nested_invalid_mixed_passive():
    def _test_func(i: Dict[str, int], j: List[int] = 0) -> Tuple[Tuple[int, int], int]:
        """Function that adds two numbers and returns the result.

        :param i: the first number
        :type i: Dict[str, str]
        :param j: the second number
        :type j: List[str]
        :return: Result of addition between `i` and `j`.
        :rtype: Tuple[Tuple[str, str], str]
        """
        return ((i + j, i + j + 1), i)

    i, j = 2, 2
    parsed_docstring = parse_docstring(_test_func, dialect="rest")
    type_check_results = type_check_arguments(
        parsed_docstring["types"],
        parameters={"i": {"first": i}, "j": [0, j]},
    )
    assert not type_check_results["i"].result
    assert list(
        (item.result, item.expected, item.actual)
        for item in type_check_results["i"]._subitems
    ) == [(True, "str", "str"), (False, "str", "int")]

    assert not type_check_results["j"].result
    assert list(
        (item.result, item.expected, item.actual)
        for item in type_check_results["j"]._subitems
    ) == [(False, "str", "int"), (False, "str", "int")]

    result = _test_func(i, j)
    type_check_returns = type_check_rtypes(parsed_docstring["rtypes"], results=result)
    assert not type_check_returns.result
    assert list(
        (item.result, item.expected, item.actual)
        for item in type_check_returns._subitems
    ) == [(False, "tuple", "tuple"), (False, "str", "int")]
    assert list(
        (item.result, item.expected, item.actual)
        for item in type_check_returns._subitems[0]._subitems
    ) == [(False, "str", "int"), (False, "str", "int")]

    assert result == ((4, 5), 2)


def test_type_check_google_style_nested_invalid_mixed_passive():
    def _test_func(i: Dict[str, int], j: List[int] = 0) -> Tuple[Tuple[int, int], int]:
        """Function that adds two numbers and returns the result.

        Args:
            i: the first number
            j: the second number

        Types:
            i: Dict[str, str]
            j: List[str]

        Returns:
            Result of addition between `i` and `j`.

        Return Type:
            Tuple[Tuple[str, str], str]
        """
        return ((i + j, i + j + 1), i)

    i, j = 2, 2
    parsed_docstring = parse_docstring(_test_func, dialect="google")
    type_check_results = type_check_arguments(
        parsed_docstring["types"],
        parameters={"i": {"first": i}, "j": [0, j]},
    )
    assert not type_check_results["i"].result
    assert list(
        (item.result, item.expected, item.actual)
        for item in type_check_results["i"]._subitems
    ) == [(True, "str", "str"), (False, "str", "int")]

    assert not type_check_results["j"].result
    assert list(
        (item.result, item.expected, item.actual)
        for item in type_check_results["j"]._subitems
    ) == [(False, "str", "int"), (False, "str", "int")]

    result = _test_func(i, j)
    type_check_returns = type_check_rtypes(parsed_docstring["rtypes"], results=result)
    assert not type_check_returns.result
    assert list(
        (item.result, item.expected, item.actual)
        for item in type_check_returns._subitems
    ) == [(False, "tuple", "tuple"), (False, "str", "int")]
    assert list(
        (item.result, item.expected, item.actual)
        for item in type_check_returns._subitems[0]._subitems
    ) == [(False, "str", "int"), (False, "str", "int")]

    assert result == ((4, 5), 2)


def test_type_check_numpydoc_style_nested_invalid_mixed_passive():
    def _test_func(i: Dict[str, int], j: List[int] = 0) -> Tuple[Tuple[int, int], int]:
        """Function that adds two numbers and returns the result.

        Parameters
        ----------
        i:
            the first number
        j:
            the second number

        Types
        -----
        i:
            Dict[str, str]
        j:
            List[str]

        Returns
        -------
            Result of addition between `i` and `j`.

        Return Type
        -----------
            Tuple[Tuple[str, str], str]
        """
        return ((i + j, i + j + 1), i)

    with pytest.raises(NotImplementedError):
        i, j = 2, 2
        parsed_docstring = parse_docstring(_test_func, dialect="numpydoc")
        type_check_results = type_check_arguments(
            parsed_docstring["types"],
            parameters={"i": {"first": i}, "j": [0, j]},
        )
        assert not type_check_results["i"].result
        assert list(
            (item.result, item.expected, item.actual)
            for item in type_check_results["i"]._subitems
        ) == [(True, "str", "str"), (False, "str", "int")]

        assert not type_check_results["j"].result
        assert list(
            (item.result, item.expected, item.actual)
            for item in type_check_results["j"]._subitems
        ) == [(False, "str", "int"), (False, "str", "int")]

        result = _test_func(i, j)
        type_check_returns = type_check_rtypes(
            parsed_docstring["rtypes"], results=result
        )
        assert not type_check_returns.result
        assert list(
            (item.result, item.expected, item.actual)
            for item in type_check_returns._subitems
        ) == [(False, "tuple", "tuple"), (False, "str", "int")]
        assert list(
            (item.result, item.expected, item.actual)
            for item in type_check_returns._subitems[0]._subitems
        ) == [(False, "str", "int"), (False, "str", "int")]

        assert result == ((4, 5), 2)
