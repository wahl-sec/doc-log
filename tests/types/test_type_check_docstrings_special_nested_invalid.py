#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest

from doc_log.parser import parse_docstring
from doc_log.types import type_check_arguments, type_check_rtypes


def test_type_check_pep257_style_invalid_special_nested_passive():
    def _test_func(i, j=0):
        """Function that adds two numbers and returns the result.

        Arguments:
        i -- the first number

        Types:
        i -- Optional[Union[Union[str, int], float]]
        j -- Optional[int]

        Keyword Arguments:
        j -- the second number (default 0)

        Returns:
        Result of addition between `i` and `j`.

        Return Type:
        Optional[Union[int, float]]
        """
        if isinstance(i, bool):
            if not i:
                return "STR"

            i = 2

        if isinstance(j, str):
            j = int(j)

        return str(i + j)

    for i, j, _result in ((True, "2", "4"), (False, 2.2, "STR")):
        parsed_docstring = parse_docstring(_test_func, dialect="pep257")
        type_check_results = type_check_arguments(
            parsed_docstring["types"],
            parameters={"i": i, "j": j},
        )
        assert not type_check_results["i"].result
        assert type_check_results["i"].expected == "Optional"
        assert not type_check_results["j"].result
        assert type_check_results["j"].expected == "Optional"

        result = _test_func(i, j)
        type_check_returns = type_check_rtypes(
            parsed_docstring["rtypes"], results=result
        )

        assert not type_check_returns.result
        assert type_check_returns.expected == "Optional"

        assert result == _result


def test_type_check_epytext_style_invalid_special_nested_passive():
    def _test_func(i, j):
        """
        Function that adds two numbers and returns the result.

        @param i: the first number
        @type i: Optional[Union[Union[str, int], float]]
        @param j: the second number
        @type j: Optional[int]
        @return: Result of addition between `i` and `j`.
        @rtype: Optional[Union[int, float]]
        """
        if isinstance(i, bool):
            if not i:
                return "STR"

            i = 2

        if isinstance(j, str):
            j = int(j)

        return str(i + j)

    for i, j, _result in ((True, "2", "4"), (False, 2.2, "STR")):
        parsed_docstring = parse_docstring(_test_func, dialect="epytext")
        type_check_results = type_check_arguments(
            parsed_docstring["types"],
            parameters={"i": i, "j": j},
        )
        assert not type_check_results["i"].result
        assert type_check_results["i"].expected == "Optional"
        assert not type_check_results["j"].result
        assert type_check_results["j"].expected == "Optional"

        result = _test_func(i, j)
        type_check_returns = type_check_rtypes(
            parsed_docstring["rtypes"], results=result
        )

        assert not type_check_returns.result
        assert type_check_returns.expected == "Optional"

        assert result == _result


def test_type_check_rest_style_invalid_special_nested_passive():
    def _test_func(i, j):
        """Function that adds two numbers and returns the result.

        :param i: the first number
        :type i: Optional[Union[Union[str, int], float]]
        :param j: the second number
        :type j: Optional[int]
        :return: Result of addition between `i` and `j`.
        :rtype: Optional[Union[int, float]]
        """
        if isinstance(i, bool):
            if not i:
                return "STR"

            i = 2

        if isinstance(j, str):
            j = int(j)

        return str(i + j)

    for i, j, _result in ((True, "2", "4"), (False, 2.2, "STR")):
        parsed_docstring = parse_docstring(_test_func, dialect="rest")
        type_check_results = type_check_arguments(
            parsed_docstring["types"],
            parameters={"i": i, "j": j},
        )
        assert not type_check_results["i"].result
        assert type_check_results["i"].expected == "Optional"
        assert not type_check_results["j"].result
        assert type_check_results["j"].expected == "Optional"

        result = _test_func(i, j)
        type_check_returns = type_check_rtypes(
            parsed_docstring["rtypes"], results=result
        )

        assert not type_check_returns.result
        assert type_check_returns.expected == "Optional"

        assert result == _result


def test_type_check_google_style_invalid_special_nested_passive():
    def _test_func(i, j):
        """Function that adds two numbers and returns the result.

        Args:
            i: the first number
            j: the second number

        Types:
            i: Optional[Union[Union[str, int], float]]
            j: Optional[int]

        Returns:
            Result of addition between `i` and `j`.

        Return Type:
            Optional[Union[int, float]]
        """
        if isinstance(i, bool):
            if not i:
                return "STR"

            i = 2

        if isinstance(j, str):
            j = int(j)

        return str(i + j)

    for i, j, _result in ((True, "2", "4"), (False, 2.2, "STR")):
        parsed_docstring = parse_docstring(_test_func, dialect="google")
        type_check_results = type_check_arguments(
            parsed_docstring["types"],
            parameters={"i": i, "j": j},
        )
        assert not type_check_results["i"].result
        assert type_check_results["i"].expected == "Optional"
        assert not type_check_results["j"].result
        assert type_check_results["j"].expected == "Optional"

        result = _test_func(i, j)
        type_check_returns = type_check_rtypes(
            parsed_docstring["rtypes"], results=result
        )

        assert not type_check_returns.result
        assert type_check_returns.expected == "Optional"

        assert result == _result


def test_type_check_numpydoc_style_invalid_special_nested_passive():
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
            Optional[Union[Union[str, int], float]]
        j:
            Optional[int]

        Returns
        -------
            Result of addition between `i` and `j`.

        Return Types
        ------------
            Optional[Union[int, float]]
        """
        if isinstance(i, bool):
            if not i:
                return "STR"

            i = 2

        if isinstance(j, str):
            j = int(j)

        return str(i + j)

    with pytest.raises(NotImplementedError):
        for i, j, _result in ((True, "2", "4"), (False, 2.2, "STR")):
            parsed_docstring = parse_docstring(_test_func, dialect="numpydoc")
            type_check_results = type_check_arguments(
                parsed_docstring["types"],
                parameters={"i": i, "j": j},
            )
            assert not type_check_results["i"].result
            assert type_check_results["i"].expected == "Optional"
            assert not type_check_results["j"].result
            assert type_check_results["j"].expected == "Optional"

            result = _test_func(i, j)
            type_check_returns = type_check_rtypes(
                parsed_docstring["rtypes"], results=result
            )

            assert not type_check_returns.result
            assert type_check_returns.expected == "Optional"

            assert result == _result
