#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest

from doc_log import doc_log


def test_wrapper_pep257_style_simple_active():
    @doc_log(dialect="pep257", type_check=True, _active_type_check=True)
    def _test_func(i, j=0) -> int:
        """Function that adds two numbers and returns the result.

        Arguments:
        i -- the first number

        Keyword Arguments:
        j -- the second number (default 0)

        Types:
        i -- int
        j -- int

        Returns:
        Result of addition between `i` and `j`.

        Return Type:
        int
        """
        return i + j

    with pytest.raises(TypeError):
        assert _test_func("2") == 2


def test_wrapper_epytext_style_simple_passive():
    @doc_log(dialect="epytext", type_check=True, _active_type_check=True)
    def _test_func(i, j=0) -> int:
        """
        Function that adds two numbers and returns the result.

        @param i: the first number
        @type i: int
        @param j: the second number
        @type j: int
        @return: Result of addition between `i` and `j`.
        @rtype: int
        """
        return i + j

    with pytest.raises(TypeError):
        assert _test_func("2") == 2


def test_wrapper_rest_style_simple_passive():
    @doc_log(dialect="rest", type_check=True, _active_type_check=True)
    def _test_func(i, j=0) -> int:
        """Function that adds two numbers and returns the result.

        :param i: the first number
        :type i: int
        :param j: the second number
        :type j: int
        :return: Result of addition between `i` and `j`.
        :rtype: int
        """
        return i + j

    with pytest.raises(TypeError):
        assert _test_func("2") == 2


def test_wrapper_google_style_simple_passive():
    @doc_log(dialect="google", type_check=True, _active_type_check=True)
    def _test_func(i, j=0) -> int:
        """Function that adds two numbers and returns the result.

        Args:
            i: the first number
            j: the second number

        Types:
            i: int
            j: int

        Returns:
            Result of addition between `i` and `j`.

        Return Type:
            int
        """
        return i + j

    with pytest.raises(TypeError):
        assert _test_func("2") == 2


def test_wrapper_numpydoc_style_simple_passive():
    @doc_log(dialect="numpydoc", type_check=True, _active_type_check=True)
    def _test_func(i, j=0) -> int:
        """Function that adds two numbers and returns the result.

        Parameters
        ----------
        i : int
            the first number
        j : int
            the second number

        Returns
        -------
        int
            Result of addition between `i` and `j`.
        """
        return i + j

    with pytest.raises(NotImplementedError):
        assert _test_func(2) == 2
