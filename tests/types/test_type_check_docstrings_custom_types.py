#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest

from doc_log.parser import parse_docstring
from doc_log.types import type_check_arguments, type_check_rtypes


class Adder:
    def __init__(self, value):
        self.value = value

    def __add__(self, other):
        return self.value + other.value + 1


def test_type_check_pep257_style_custom_types_passive():
    def _test_func(i, j=0) -> Adder:
        """Function that adds two `Adders` and returns a new `Adder` with the result.

        Arguments:
        i -- the first `Adder`

        Keyword Arguments:
        j -- the second `Adder` (default 0)

        Types:
        i -- Adder
        j -- Adder

        Returns:
        Result of addition between `i` and `j`.

        Return Type:
        Adder
        """
        return Adder(i + j)

    i, j = Adder(2), Adder(2)
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
    type_check_returns = type_check_rtypes(parsed_docstring["rtypes"], results=result)

    assert type_check_returns.result
    assert (
        type(result).__name__
        == type_check_returns.expected
        == type_check_returns.actual
    )

    assert result.value == 5


def test_type_check_epytext_style_custom_types_passive():
    def _test_func(i, j):
        """Function that adds two `Adders` and returns a new `Adder` with the result.

        @param i: the first `Adder`
        @type i: Adder
        @param j: the second `Adder`
        @type j: Adder
        @return: Result of addition between `i` and `j`.
        @rtype: Adder
        """
        return Adder(i + j)

    i, j = Adder(2), Adder(2)
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
    type_check_returns = type_check_rtypes(parsed_docstring["rtypes"], results=result)

    assert type_check_returns.result
    assert (
        type(result).__name__
        == type_check_returns.expected
        == type_check_returns.actual
    )

    assert result.value == 5


def test_type_check_rest_style_custom_types_passive():
    def _test_func(i, j) -> int:
        """Function that adds two `Adders` and returns a new `Adder` with the result.

        :param i: the first `Adder`
        :type i: Adder
        :param j: the second `Adder`
        :type j: Adder
        :return: Result of addition between `i` and `j`.
        :rtype: Adder
        """
        return Adder(i + j)

    i, j = Adder(2), Adder(2)
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
    type_check_returns = type_check_rtypes(parsed_docstring["rtypes"], results=result)

    assert type_check_returns.result
    assert (
        type(result).__name__
        == type_check_returns.expected
        == type_check_returns.actual
    )

    assert result.value == 5


def test_type_check_google_style_custom_types_passive():
    def _test_func(i, j) -> int:
        """Function that adds two `Adders` and returns a new `Adder` with the result.

        Args:
            i: the first `Adder`
            j: the second `Adder`

        Types:
            i: Adder
            j: Adder

        Returns:
            Result of addition between `i` and `j`.

        Return Type:
            Adder
        """
        return Adder(i + j)

    i, j = Adder(2), Adder(2)
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
    type_check_returns = type_check_rtypes(parsed_docstring["rtypes"], results=result)

    assert type_check_returns.result
    assert (
        type(result).__name__
        == type_check_returns.expected
        == type_check_returns.actual
    )

    assert result.value == 5


def test_type_check_numpydoc_style_custom_types_passive():
    def _test_func(i, j) -> int:
        """Function that adds two `Adders` and returns a new `Adder` with the result.

        Parameters
        ----------
        i : Adder
            the first `Adder`
        j : Adder
            the second `Adder`

        Returns
        -------
        Adder
            Result of addition between `i` and `j`.
        """
        return Adder(i + j)

    with pytest.raises(NotImplementedError):
        i, j = Adder(2), Adder(2)
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
            parsed_docstring["rtypes"], results=result
        )

        assert type_check_returns.result
        assert (
            type(result).__name__
            == type_check_returns.expected
            == type_check_returns.actual
        )

        assert result.value == 5
