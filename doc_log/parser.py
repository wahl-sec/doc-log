#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from re import compile
from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class PatternDescriptor:
    """Describes the section pattern and the display value that represents the section."""

    pattern: str


@dataclass
class SectionPattern:
    """Describes the section syntax, i.e the name of the section like arguments, raises etc.
    The name of the parameter if applicable for example i in the following example, this can be None
    if no name is present.
    The value of the parameter i.e parameter i in the following example.

    ```
    :param i: parameter i
    ```
    """

    section: PatternDescriptor
    value: str
    name: Optional[str] = None


@dataclass
class SectionItem:
    """Describes the actual section item, that is the name (if applicable) and the value for the item."""

    value: str
    name: Optional[str] = None


@dataclass
class Section:
    """Describes the actual section, that is the name of the section and the items belonging to the section."""

    section: str
    items: List[SectionItem]


def parse_docstring(docstring: str, dialect: str) -> Dict[str, str]:
    """Parse the docstring and extract the rules related to doc-log.

    :param docstring: The docstring to extract rules from.
    :type docstring: str
    :param dialect: The dialect of the docstring to parse.
    :type dialect: str
    :returns: The rules extracted from the docstring.
    :rtype: Dict[str, str]
    """

    def _parse_section_indexes(
        docstring: List[str],
        sections: Dict[str, SectionPattern],
    ) -> Dict[int, str]:
        """Generate the indexes at which each section begins, and return the results.

        :param docstring: The docstring to parse the section indexes from.
        :type docstring: List[str]
        :param sections: The sections that should be parsed from the docstring if they exist.
        :type sections: Dict[str, SectionPattern]
        :return: The section indexes that were identified from the provided sections.
        :rtype: Dict[int, str]
        """

        _section_indexes = {}
        for index, line in enumerate(docstring):
            docstring[index] = line.strip()
            for section, patterns in sections.items():
                if (
                    compile(patterns.section.pattern).search(docstring[index])
                    is not None
                ):
                    _section_indexes[index] = section

        return _section_indexes

    def _collect_sections(
        docstring: List[str],
        section_indexes: Dict[int, str],
        sections: Dict[str, SectionPattern],
    ) -> Dict[str, SectionPattern]:
        """Parse and collect all section items and define the name (if available) and the value of item.
        Then group all the items in their respective sections.

        :param docstring: The docstring to parse the section items from.
        :type docstring: List[str]
        :param section_indexes: The indexes defining where each item begins.
        :type section_indexes: Dict[int, str]
        :param sections: The sections that define each sections patterns.
        :type sections: Dict[str, SectionPattern]
        :return: The collected section items aggregated in their respective sections.
        :rtype: Dict[str, str]
        """
        _collected_sections = {
            key: Section(section=key, items=[]) for key in set(section_indexes.values())
        }
        for index in sorted(section_indexes):
            name = None
            if sections[section_indexes[index]].name is not None:
                name = compile(sections[section_indexes[index]].name).search(
                    docstring[index]
                )

                name = name.group().strip() if name is not None else None

            value = None
            if sections[section_indexes[index]].value is not None:
                value = compile(sections[section_indexes[index]].value).search(
                    docstring[index]
                )

                value = value.group().strip() if value is not None else None

            _collected_sections[section_indexes[index]].items.append(
                SectionItem(value=value, name=name)
            )

        return _collected_sections

    def _convert_to_oneline_items(
        docstring: List[str], sections: Dict[str, SectionPattern]
    ) -> List[str]:
        """Converts docstrings that are of a format similar to the example below into
        docstrings that specify items on the same line making them easier to parse.

        ```
        ...
        Arguments:
            i: test argument
        ```
        Converts into the oneline item variant.
        ```
        ...
        :arguments i: test argument
        ```

        :param docstring: The initial docstring to convert.
        :type docstring: List[str]
        :param sections: The initial sections to convert into oneline items.
        :type sections: Dict[str, SectionPattern]
        :return: The converted docstring.
        :rtype: List[str]
        """
        _section_indexes = _parse_section_indexes(
            docstring=docstring, sections=sections
        )

        _docstring = docstring[: min(_section_indexes.keys())]
        indexes = list(sorted(_section_indexes.keys()))
        for index in sorted(_section_indexes):
            if not indexes:
                break

            for _index in range(
                index + 1,
                min([val for val in indexes if val != index])
                if len(indexes) > 1
                else len(docstring),
            ):
                _docstring.append(f":{_section_indexes[index]} {docstring[_index]}")
            indexes = indexes[1:]

        return _docstring

    def _parse_multiline(
        docstring: str,
        sections: Dict[str, SectionPattern],
        _convert_to_oneline: Optional[Dict[str, Section]] = None,
    ) -> Dict[str, Section]:
        """General multiline docstring parser. Takes an initial docstring and converts it given
        the specified syntax rules as defined by the sections. Optionally convert to oneline items if provided.

        :param docstring: The multiline docstring to parse.
        :type docstring: str
        :param sections: The sections describing what sections there are and how to parse them.
        :type sections: Dict[str, SectionPattern]
        :param _convert_to_oneline: If the docstring contains multiline items then convert them given and parse using updated sections, defaults to None
        :type _convert_to_oneline: Optional[Dict[str, Section]], optional
        :return: The parsed docstring into their respective sections.
        :rtype: Dict[str, Section]
        """
        split_docstring = [line for line in docstring.split("\n") if line.strip()]
        if _convert_to_oneline is not None:
            split_docstring = _convert_to_oneline_items(
                docstring=split_docstring, sections=sections
            )
            sections = _convert_to_oneline

        section_indexes = _parse_section_indexes(
            docstring=split_docstring, sections=sections
        )

        return _collect_sections(
            docstring=split_docstring,
            section_indexes=section_indexes,
            sections=sections,
        )

    # Most of the styles were taken from PEP257,
    # https://stackoverflow.com/questions/3898572/what-is-the-standard-python-docstring-format
    def _parse_pep257_multiline(docstring: str) -> Dict[str, str]:
        """Parse docstring and extract rules from docstrings formatted by the
        multiline PEP257 standard.

        :param docstring: The docstring to extract rules from.
        :type docstring: str
        :return: The rules extracted from the docstring.
        :rtype: Dict[str, str]
        """
        sections = {
            "arguments": SectionPattern(
                section=PatternDescriptor(pattern=r"^Arguments:$"),
                name=r" .*(?=:)",
                value=r"--\ .*$",
            ),
            "keywords": SectionPattern(
                section=PatternDescriptor(pattern=r"^Keyword\ Arguments:$"),
                name=r" .*(?=:)",
                value=r"--\ .*$",
            ),
            "raises": SectionPattern(
                section=PatternDescriptor(pattern=r"^Exceptions:$"),
                name=r" .*(?=:)",
                value=r"--\ .*$",
            ),
            "returns": SectionPattern(
                section=PatternDescriptor(pattern=r"^Returns:$"),
                name=r" .*(?=:)",
                value=r"--\ .*$",
            ),
            "types": SectionPattern(
                section=PatternDescriptor(pattern=r"^Types:$"),
                name=r" .*(?=:)",
                value=r"--\ .*$",
            ),
            "rtypes": SectionPattern(
                section=PatternDescriptor(pattern=r"^Return Type:$"),
                name=r" .*(?=:)",
                value=r"--\ .*$",
            ),
        }

        sections_oneline = {
            "arguments": SectionPattern(
                section=PatternDescriptor(pattern=r"^:arguments"),
                name=r"(?<= ).*(?= --)",
                value=r"(?<=-- ).*$",
            ),
            "keywords": SectionPattern(
                section=PatternDescriptor(pattern=r"^:keywords"),
                name=r"(?<= ).*(?= --)",
                value=r"(?<=-- ).*$",
            ),
            "types": SectionPattern(
                section=PatternDescriptor(pattern=r"^:types"),
                name=r"(?<= ).*(?= --)",
                value=r"(?<=-- ).*$",
            ),
            "raises": SectionPattern(
                section=PatternDescriptor(pattern=r"^:raises"),
                name=r"(?<= ).*(?= --)",
                value=r"(?<=-- ).*$",
            ),
            "returns": SectionPattern(
                section=PatternDescriptor(pattern=r"^:returns"),
                name=r"(?<= ).*(?= --)",
                value=r"(?<=:returns ).*$",
            ),
            "rtypes": SectionPattern(
                section=PatternDescriptor(pattern=r"^:rtypes"),
                name=r"(?<= ).*(?= --)",
                value=r"(?<=:rtypes ).*$",
            ),
        }

        return _parse_multiline(
            docstring=docstring,
            sections=sections,
            _convert_to_oneline=sections_oneline,
        )

    def _parse_epytext_multiline(docstring: str) -> Dict[str, str]:
        """Parse docstring and extract rules from docstrings formatted by the
        multiline Epytext standard.

        :param docstring: The docstring to extract rules from.
        :type docstring: str
        :return: The rules extracted from the docstring.
        :rtype: Dict[str, str]
        """
        sections = {
            "arguments": SectionPattern(
                section=PatternDescriptor(pattern=r"^@param"),
                name=r"(?<= ).*(?=:)",
                value=r"(?<=:) .*$",
            ),
            "types": SectionPattern(
                section=PatternDescriptor(pattern=r"^@type"),
                name=r"(?<= ).*(?=:)",
                value=r"(?<=:) .*$",
            ),
            "raises": SectionPattern(
                section=PatternDescriptor(pattern=r"^@raise"),
                name=r"(?<= ).*(?=:)",
                value=r"(?<=:) .*$",
            ),
            "returns": SectionPattern(
                section=PatternDescriptor(pattern=r"^@return"),
                value=r"(?<=:) .*$",
            ),
            "rtypes": SectionPattern(
                section=PatternDescriptor(pattern=r"^@rtype"),
                value=r"(?<=:) .*$",
            ),
        }

        return _parse_multiline(
            docstring=docstring,
            sections=sections,
        )

    def _parse_rest_multiline(docstring: str) -> Dict[str, str]:
        """Parse docstring and extract rules from docstrings formatted by the
        multiline reST standard.

        :param docstring: The docstring to extract rules from.
        :type docstring: str
        :return: The rules extracted from the docstring.
        :rtype: Dict[str, str]
        """
        sections = {
            "arguments": SectionPattern(
                section=PatternDescriptor(pattern=r"^:param"),
                name=r"(?<= ).*(?=:)",
                value=r"(?<=: ).*$",
            ),
            "types": SectionPattern(
                section=PatternDescriptor(pattern=r"^:type"),
                name=r"(?<= ).*(?=:)",
                value=r"(?<=: ).*$",
            ),
            "returns": SectionPattern(
                section=PatternDescriptor(pattern=r"^:return"),
                value=r"(?<=: ).*$",
            ),
            "rtypes": SectionPattern(
                section=PatternDescriptor(pattern=r"^:rtype"),
                value=r"(?<=: ).*$",
            ),
        }

        return _parse_multiline(
            docstring=docstring,
            sections=sections,
        )

    def _parse_google_multiline(docstring: str) -> Dict[str, str]:
        """Parse docstring and extract rules from docstrings formatted by the
        multiline Google standard.

        :param docstring: The docstring to extract rules from.
        :type docstring: str
        :return: The rules extracted from the docstring.
        :rtype: Dict[str, str]
        """
        sections = {
            "arguments": SectionPattern(
                section=PatternDescriptor(pattern=r"^Args:$"),
                name=r"(?<= ).*(?=:)",
                value=r"(?<=: ).*$",
            ),
            "types": SectionPattern(
                section=PatternDescriptor(pattern=r"^Types:$"),
                name=r"(?<= ).*(?=:)",
                value=r"(?<=: ).*$",
            ),
            "raises": SectionPattern(
                section=PatternDescriptor(pattern=r"^Raises:$"),
                name=r"(?<= ).*(?=:)",
                value=r"(?<=: ).*$",
            ),
            "returns": SectionPattern(
                section=PatternDescriptor(pattern=r"^Returns:$"),
                value=r"(?<=: ).*$",
            ),
            "rtypes": SectionPattern(
                section=PatternDescriptor(pattern=r"^Return Type:$"),
                value=r"(?<=: ).*$",
            ),
        }

        sections_oneline = {
            "arguments": SectionPattern(
                section=PatternDescriptor(pattern=r"^:arguments"),
                name=r"(?<= ).*(?=:)",
                value=r"(?<=: ).*$",
            ),
            "types": SectionPattern(
                section=PatternDescriptor(pattern=r"^:types"),
                name=r"(?<= ).*(?=:)",
                value=r"(?<=: ).*$",
            ),
            "raises": SectionPattern(
                section=PatternDescriptor(pattern=r"^:raises"),
                name=r"(?<= ).*(?=:)",
                value=r"(?<=: ).*$",
            ),
            "returns": SectionPattern(
                section=PatternDescriptor(pattern=r"^:returns"),
                name=r"(?<= ).*(?=:)",
                value=r"(?<=:returns ).*$",
            ),
            "rtypes": SectionPattern(
                section=PatternDescriptor(pattern=r"^:rtype"),
                name=r"(?<= ).*(?=:)",
                value=r"(?<=:rtypes ).*$",
            ),
        }

        return _parse_multiline(
            docstring=docstring,
            sections=sections,
            _convert_to_oneline=sections_oneline,
        )

    def _parse_numpydoc_multiline(docstring: str) -> Dict[str, str]:
        """Parse docstring and extract rules from docstrings formatted by the
        multiline NumpyDoc standard.

        :param docstring: The docstring to extract rules from.
        :type docstring: str
        :return: The rules extracted from the docstring.
        :rtype: Dict[str, str]
        """
        raise NotImplementedError

    if dialect.lower() == "pep257":
        return _parse_pep257_multiline(docstring)
    elif dialect.lower() == "epytext":
        return _parse_epytext_multiline(docstring)
    elif dialect.lower() == "rest":
        return _parse_rest_multiline(docstring)
    elif dialect.lower() == "google":
        return _parse_google_multiline(docstring)
    elif dialect.lower() == "numpydoc":
        return _parse_numpydoc_multiline(docstring)
    else:
        raise ValueError(
            f"Dialect type: {dialect}, expected one of `pep257`, `epytext`, `rest`, `google` or `numpydoc`"
        )
