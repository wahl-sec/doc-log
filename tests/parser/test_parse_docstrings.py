#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest

from doc_log.parser import parse_docstring


def test_parse_pep257_style_simple():
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

    parsed_docstring = parse_docstring(_test_func, dialect="pep257")
    expected = {
        "arguments": {"i": "the first number"},
        "keywords": {"j": "the second number (default 0)"},
        "types": {"i": "int", "j": "int"},
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
    assert _test_func(2, 2) == 4


def test_parse_epytext_style_simple():
    def _test_func(i, j) -> int:
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

    parsed_docstring = parse_docstring(_test_func, dialect="epytext")
    expected = {
        "arguments": {"i": "the first number", "j": "the second number"},
        "returns": {None: "Result of addition between `i` and `j`."},
        "types": {"i": "int", "j": "int"},
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
    assert _test_func(2, 2) == 4


def test_parse_rest_style_simple():
    def _test_func(i, j) -> int:
        """Function that adds two numbers and returns the result.

        :param i: the first number
        :type i: int
        :param j: the second number
        :type j: int
        :return: Result of addition between `i` and `j`.
        :rtype: int
        """
        return i + j

    parsed_docstring = parse_docstring(_test_func, dialect="rest")
    expected = {
        "arguments": {"i": "the first number", "j": "the second number"},
        "types": {"i": "int", "j": "int"},
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
    assert _test_func(2, 2) == 4


def test_parse_google_style_simple():
    def _test_func(i, j) -> int:
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

    parsed_docstring = parse_docstring(_test_func, dialect="google")
    expected = {
        "arguments": {"i": "the first number", "j": "the second number"},
        "types": {"i": "int", "j": "int"},
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
    assert _test_func(2, 2) == 4


def test_parse_numpydoc_style_simple():
    def _test_func(i, j) -> int:
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
        parsed_docstring = parse_docstring(_test_func, dialect="numpydoc")
        expected = {
            "arguments": {"i": "the first number", "j": "the second number"},
            "types": {"i": "int", "j": "int"},
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

    assert _test_func(2, 2) == 4
