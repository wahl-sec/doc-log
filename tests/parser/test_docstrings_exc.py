#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest

from doc_log.logger import parse_docstring


def test_pep257_style_simple():
    def _test_func(i, j=0) -> int:
        """Function that adds two numbers and returns the result.

        Arguments:
        i -- the first number

        Keyword Arguments:
        j -- the second number (default 0)

        Exceptions:
        ValueError -- if the first number is even

        Returns:
        Result of addition between `i` and `j`.
        """
        if i % 2 == 0:
            raise ValueError

        return i + j

    parsed_docstring = parse_docstring(_test_func.__doc__, logger="pep257")
    expected = {
        "arguments": {"i": "the first number"},
        "keywords": {"j": "the second number (default 0)"},
        "raises": {"ValueError": "if the first number is even"},
        "returns": {None: "Result of addition between `i` and `j`."},
    }

    assert all(
        [
            section_name in expected and section_name == section.section
            for section_name, section in parsed_docstring.items()
        ]
    )
    assert all(
        [
            all([expected_items[item.name] == item.value for item in section_items])
            and set(expected_items.keys()) == set([item.name for item in section_items])
            and len(expected_items.keys()) == len([item.name for item in section_items])
            for expected_items, section_items in [
                (expected[section.section], section.items)
                for section in parsed_docstring.values()
            ]
        ]
    )
    with pytest.raises(ValueError):
        _test_func(2, 2)


def test_epytext_style_simple():
    def _test_func(i, j) -> int:
        """
        Function that adds two numbers and returns the result.

        @param i: the first number
        @param j: the second number
        @raise ValueError: if the first number is even
        @return: Result of addition between `i` and `j`.
        """
        if i % 2 == 0:
            raise ValueError

        return i + j

    parsed_docstring = parse_docstring(_test_func.__doc__, logger="epytext")
    expected = {
        "arguments": {"i": "the first number", "j": "the second number"},
        "raises": {"ValueError": "if the first number is even"},
        "returns": {None: "Result of addition between `i` and `j`."},
    }

    assert all(
        [
            section_name in expected and section_name == section.section
            for section_name, section in parsed_docstring.items()
        ]
    )
    assert all(
        [
            all([expected_items[item.name] == item.value for item in section_items])
            and set(expected_items.keys()) == set([item.name for item in section_items])
            and len(expected_items.keys()) == len([item.name for item in section_items])
            for expected_items, section_items in [
                (expected[section.section], section.items)
                for section in parsed_docstring.values()
            ]
        ]
    )
    with pytest.raises(ValueError):
        _test_func(2, 2)


def test_rest_style_simple():
    def _test_func(i, j) -> int:
        """Function that adds two numbers and returns the result.

        :param i: the first number
        :type i: int
        :param j: the second number
        :type j: int
        :raises ValueError: if the first number is even
        :return: Result of addition between `i` and `j`.
        :rtype: int
        """
        if i % 2 == 0:
            raise ValueError

        return i + j

    parsed_docstring = parse_docstring(_test_func.__doc__, logger="rest")
    expected = {
        "arguments": {"i": "the first number", "j": "the second number"},
        "types": {"i": "int", "j": "int"},
        "raises": {"ValueError": "if the first number is even"},
        "returns": {None: "Result of addition between `i` and `j`."},
        "rtypes": {None: "int"},
    }

    assert all(
        [
            section_name in expected and section_name == section.section
            for section_name, section in parsed_docstring.items()
        ]
    )
    assert all(
        [
            all([expected_items[item.name] == item.value for item in section_items])
            and set(expected_items.keys()) == set([item.name for item in section_items])
            and len(expected_items.keys()) == len([item.name for item in section_items])
            for expected_items, section_items in [
                (expected[section.section], section.items)
                for section in parsed_docstring.values()
            ]
        ]
    )
    with pytest.raises(ValueError):
        _test_func(2, 2)


def test_google_style_simple():
    def _test_func(i, j) -> int:
        """Function that adds two numbers and returns the result.

        Args:
            i: the first number
            j: the second number

        Raises:
            ValueError: if the first number is even

        Returns:
            Result of addition between `i` and `j`.
        """
        if i % 2 == 0:
            raise ValueError

        return i + j

    parsed_docstring = parse_docstring(_test_func.__doc__, logger="google")
    expected = {
        "arguments": {"i": "the first number", "j": "the second number"},
        "raises": {"ValueError": "if the first number is even"},
        "returns": {None: "Result of addition between `i` and `j`."},
    }

    assert all(
        [
            section_name in expected and section_name == section.section
            for section_name, section in parsed_docstring.items()
        ]
    )
    assert all(
        [
            all([expected_items[item.name] == item.value for item in section_items])
            and set(expected_items.keys()) == set([item.name for item in section_items])
            and len(expected_items.keys()) == len([item.name for item in section_items])
            for expected_items, section_items in [
                (expected[section.section], section.items)
                for section in parsed_docstring.values()
            ]
        ]
    )
    with pytest.raises(ValueError):
        _test_func(2, 2)


def test_numpydoc_style_simple():
    def _test_func(i, j) -> int:
        """Function that adds two numbers and returns the result.

        Parameters
        ----------
        i : int
            the first number
        j : int
            the second number

        Raises
        ------
        ValueError
            if the first number is even

        Returns
        -------
        int
            Result of addition between `i` and `j`.
        """
        if i % 2 == 0:
            raise ValueError

        return i + j

    with pytest.raises(NotImplementedError):
        parsed_docstring = parse_docstring(_test_func.__doc__, logger="numpydoc")
        expected = {
            "arguments": {"i": "the first number", "j": "the second number"},
            "types": {"i": "int", "j": "int"},
            "raises": {"ValueError": "if the first number is even"},
            "returns": {None: "Result of addition between `i` and `j`."},
            "rtypes": {None: "int"},
        }

        assert all(
            [
                section_name in expected and section_name == section.section
                for section_name, section in parsed_docstring.items()
            ]
        )
        assert all(
            [
                all([expected_items[item.name] == item.value for item in section_items])
                and set(expected_items.keys())
                == set([item.name for item in section_items])
                and len(expected_items.keys())
                == len([item.name for item in section_items])
                for expected_items, section_items in [
                    (expected[section.section], section.items)
                    for section in parsed_docstring.values()
                ]
            ]
        )

    with pytest.raises(ValueError):
        _test_func(2, 2)
