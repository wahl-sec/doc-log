#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest

from doc_log.parser import parse_docstring
from doc_log.types import type_check_arguments, type_check_rtypes


def test_type_check_pep257_style_mixed_passive():
    def _test_func(i: int, j=0) -> int:
        """Function that adds two numbers and returns the result.

        Arguments:
        i -- the first number

        Types:
        j -- int

        Keyword Arguments:
        j -- the second number (default 0)

        Returns:
        Result of addition between `i` and `j`.

        Return Type:
        int
        """
        return i + j

    i, j = 2, 2
    parsed_docstring = parse_docstring(_test_func, dialect="pep257")
    type_check_results = type_check_arguments(
        parsed_docstring["types"],
        parameters={"i": i, "j": j},
    )
    assert type_check_results["i"].result
    assert type_check_results["i"].expected == type_check_results["i"].actual
    assert type_check_results["j"].result
    assert type_check_results["j"].expected == type_check_results["j"].actual

    result = _test_func(i, j)
    type_check_returns = type_check_rtypes(parsed_docstring["rtypes"], results=[result])
    assert len(type_check_returns) == 1
    assert type_check_returns[0].result
    assert (
        type(result).__name__
        == type_check_returns[0].expected
        == type_check_returns[0].actual
    )

    assert result == 4


def test_type_check_epytext_style_mixed_passive():
    def _test_func(i: int, j) -> int:
        """
        Function that adds two numbers and returns the result.

        @param i: the first number
        @param j: the second number
        @type j: int
        @return: Result of addition between `i` and `j`.
        @rtype: int
        """
        return i + j

    i, j = 2, 2
    parsed_docstring = parse_docstring(_test_func, dialect="epytext")
    type_check_results = type_check_arguments(
        parsed_docstring["types"],
        parameters={"i": i, "j": j},
    )
    assert type_check_results["i"].result
    assert type_check_results["i"].expected == type_check_results["i"].actual
    assert type_check_results["j"].result
    assert type_check_results["j"].expected == type_check_results["j"].actual

    result = _test_func(i, j)
    type_check_returns = type_check_rtypes(parsed_docstring["rtypes"], results=[result])
    assert len(type_check_returns) == 1
    assert type_check_returns[0].result
    assert (
        type(result).__name__
        == type_check_returns[0].expected
        == type_check_returns[0].actual
    )

    assert result == 4


def test_type_check_rest_style_mixed_passive():
    def _test_func(i: int, j) -> int:
        """Function that adds two numbers and returns the result.

        :param i: the first number
        :param j: the second number
        :type j: int
        :return: Result of addition between `i` and `j`.
        :rtype: int
        """
        return i + j

    i, j = 2, 2
    parsed_docstring = parse_docstring(_test_func, dialect="rest")
    type_check_results = type_check_arguments(
        parsed_docstring["types"],
        parameters={"i": i, "j": j},
    )
    assert type_check_results["i"].result
    assert type_check_results["i"].expected == type_check_results["i"].actual
    assert type_check_results["j"].result
    assert type_check_results["j"].expected == type_check_results["j"].actual

    result = _test_func(i, j)
    type_check_returns = type_check_rtypes(parsed_docstring["rtypes"], results=[result])
    assert len(type_check_returns) == 1
    assert type_check_returns[0].result
    assert (
        type(result).__name__
        == type_check_returns[0].expected
        == type_check_returns[0].actual
    )

    assert result == 4


def test_type_check_google_style_mixed_passive():
    def _test_func(i: int, j) -> int:
        """Function that adds two numbers and returns the result.

        Args:
            i: the first number
            j: the second number

        Types:
            j: int

        Returns:
            Result of addition between `i` and `j`.

        Return Types:
            int
        """
        return i + j

    i, j = 2, 2
    parsed_docstring = parse_docstring(_test_func, dialect="google")
    type_check_results = type_check_arguments(
        parsed_docstring["types"],
        parameters={"i": i, "j": j},
    )
    assert type_check_results["i"].result
    assert type_check_results["i"].expected == type_check_results["i"].actual
    assert type_check_results["j"].result
    assert type_check_results["j"].expected == type_check_results["j"].actual

    result = _test_func(i, j)
    type_check_returns = type_check_rtypes(parsed_docstring["rtypes"], results=[result])
    assert len(type_check_returns) == 1
    assert type_check_returns[0].result
    assert (
        type(result).__name__
        == type_check_returns[0].expected
        == type_check_returns[0].actual
    )

    assert result == 4


def test_type_check_numpydoc_style_mixed_passive():
    def _test_func(i: int, j) -> int:
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
            int

        Returns
        -------
            Result of addition between `i` and `j`.

        Return Types
        ------------
            int
        """
        return i + j

    with pytest.raises(NotImplementedError):
        i, j = 2, 2
        parsed_docstring = parse_docstring(_test_func, dialect="numpydoc")
        type_check_results = type_check_arguments(
            parsed_docstring["types"],
            parameters={"i": i, "j": j},
        )
        assert type_check_results["i"].result
        assert type_check_results["i"].expected == type_check_results["i"].actual
        assert type_check_results["j"].result
        assert type_check_results["j"].expected == type_check_results["j"].actual

        result = _test_func(i, j)
        type_check_returns = type_check_rtypes(
            parsed_docstring["rtypes"], results=[result]
        )
        assert len(type_check_returns) == 1
        assert type_check_returns[0].result
        assert (
            type(result).__name__
            == type_check_returns[0].expected
            == type_check_returns[0].actual
        )

        assert result == 4
