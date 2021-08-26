#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest

from doc_log.parser import parse_docstring
from doc_log.types import type_check_arguments, type_check_rtypes


def test_type_check_pep257_style_special_passive():
    def _test_func(i, j=0):
        """Function that adds two numbers and returns the result.

        Arguments:
        i -- the first number

        Types:
        i -- Union[int, float]
        j -- Optional[int]

        Keyword Arguments:
        j -- the second number (default 0)

        Returns:
        Result of addition between `i` and `j`.

        Return Type:
        Union[int, float]
        """
        if j is None:
            j = 2
        return i + j

    for i, j, _result in ((2, 2, 4), (2.2, None, 4.2)):
        parsed_docstring = parse_docstring(_test_func, dialect="pep257")
        type_check_results = type_check_arguments(
            parsed_docstring["types"],
            parameters={"i": i, "j": j},
        )
        assert type_check_results["i"].result
        assert type_check_results["i"].expected == "Union"
        assert type_check_results["j"].result
        assert type_check_results["j"].expected == "Optional"

        result = _test_func(i, j)
        type_check_returns = type_check_rtypes(
            parsed_docstring["rtypes"], results=result
        )

        assert type_check_returns.result
        assert type_check_returns.expected == "Union"

        assert result == _result


def test_type_check_epytext_style_special_passive():
    def _test_func(i, j):
        """
        Function that adds two numbers and returns the result.

        @param i: the first number
        @type i: Union[int, float]
        @param j: the second number
        @type j: Optional[int]
        @return: Result of addition between `i` and `j`.
        @rtype: Union[int, float]
        """
        if j is None:
            j = 2
        return i + j

    for i, j, _result in ((2, 2, 4), (2.2, None, 4.2)):
        parsed_docstring = parse_docstring(_test_func, dialect="epytext")
        type_check_results = type_check_arguments(
            parsed_docstring["types"],
            parameters={"i": i, "j": j},
        )
        assert type_check_results["i"].result
        assert type_check_results["i"].expected == "Union"
        assert type_check_results["j"].result
        assert type_check_results["j"].expected == "Optional"

        result = _test_func(i, j)
        type_check_returns = type_check_rtypes(
            parsed_docstring["rtypes"], results=result
        )

        assert type_check_returns.result
        assert type_check_returns.expected == "Union"

        assert result == _result


def test_type_check_rest_style_special_passive():
    def _test_func(i, j):
        """Function that adds two numbers and returns the result.

        :param i: the first number
        :type i: Union[int, float]
        :param j: the second number
        :type j: Optional[int]
        :return: Result of addition between `i` and `j`.
        :rtype: Union[int, float]
        """
        if j is None:
            j = 2
        return i + j

    for i, j, _result in ((2, 2, 4), (2.2, None, 4.2)):
        parsed_docstring = parse_docstring(_test_func, dialect="rest")
        type_check_results = type_check_arguments(
            parsed_docstring["types"],
            parameters={"i": i, "j": j},
        )
        assert type_check_results["i"].result
        assert type_check_results["i"].expected == "Union"
        assert type_check_results["j"].result
        assert type_check_results["j"].expected == "Optional"

        result = _test_func(i, j)
        type_check_returns = type_check_rtypes(
            parsed_docstring["rtypes"], results=result
        )

        assert type_check_returns.result
        assert type_check_returns.expected == "Union"

        assert result == _result


def test_type_check_google_style_special_passive():
    def _test_func(i, j):
        """Function that adds two numbers and returns the result.

        Args:
            i: the first number
            j: the second number

        Types:
            i: Union[int, float]
            j: Optional[int]

        Returns:
            Result of addition between `i` and `j`.

        Return Type:
            Union[int, float]
        """
        if j is None:
            j = 2
        return i + j

    for i, j, _result in ((2, 2, 4), (2.2, None, 4.2)):
        parsed_docstring = parse_docstring(_test_func, dialect="google")
        type_check_results = type_check_arguments(
            parsed_docstring["types"],
            parameters={"i": i, "j": j},
        )
        assert type_check_results["i"].result
        assert type_check_results["i"].expected == "Union"
        assert type_check_results["j"].result
        assert type_check_results["j"].expected == "Optional"

        result = _test_func(i, j)
        type_check_returns = type_check_rtypes(
            parsed_docstring["rtypes"], results=result
        )

        assert type_check_returns.result
        assert type_check_returns.expected == "Union"

        assert result == _result


def test_type_check_numpydoc_style_special_passive():
    def _test_func(i, j):
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
            Union[int, float]
        j:
            Optional[int]

        Returns
        -------
            Result of addition between `i` and `j`.

        Return Types
        ------------
            Union[int, float]
        """
        if j is None:
            j = 2
        return i + j

    with pytest.raises(NotImplementedError):
        for i, j, _result in ((2, 2, 4), (2.2, None, 4.2)):
            parsed_docstring = parse_docstring(_test_func, dialect="numpydoc")
            type_check_results = type_check_arguments(
                parsed_docstring["types"],
                parameters={"i": i, "j": j},
            )
            assert type_check_results["i"].result
            assert type_check_results["i"].expected == "Union"
            assert type_check_results["j"].result
            assert type_check_results["j"].expected == "Optional"

            result = _test_func(i, j)
            type_check_returns = type_check_rtypes(
                parsed_docstring["rtypes"], results=result
            )

            assert type_check_returns.result
            assert type_check_returns.expected == "Union"

            assert result == _result
