#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from re import compile
from inspect import FrameInfo, getmodule, signature, stack
from dataclasses import dataclass
from typing import (
    Callable,
    Dict,
    List,
    Optional,
    Tuple,
    Union,
    Any,
    _SpecialForm,
    TypeVar,
)
import logging
import typing

LOGGER = logging.getLogger()


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
    _subitems: Optional[List["SectionItem"]]
    name: Optional[str] = None

    def __str__(self: "SectionItem") -> str:
        def _unfold(items: List["SectionItem"], _result: str = "") -> str:
            for item in items:
                if item._subitems:
                    _result = "{!s}[{!s}]".format(
                        item.value, _unfold(item._subitems, _result=_result)
                    )
                else:
                    if not _result:
                        _result = item.value
                    else:
                        _result = "{!s}, {!s}".format(_result, item.value)

            return _result

        if self._subitems:
            return "{!s}[{!s}]".format(self.value, _unfold(self._subitems))

        return self.value


@dataclass
class Section:
    """Describes the actual section, that is the name of the section and the items belonging to the section."""

    section: str
    items: List[SectionItem]


def parse_docstring(_function: Callable, dialect: str) -> Dict[str, str]:
    """Parse the docstring and extract the rules related to doc-log.

    :param _function: The called function that should be inspected for docstring and type hints.
    :type _function: Callable
    :param dialect: The dialect of the docstring to parse.
    :type dialect: str
    :returns: The rules extracted from the docstring.
    :rtype: Dict[str, str]
    """
    LOGGER.debug(
        "(doc-log) parsing docstring with dialect: `{!s}` from function: `{!s}` in `{!s}`".format(
            dialect, _function.__name__, getmodule(_function).__file__
        )
    )

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

    def _sanitize_type_hint(type_hint: str) -> str:
        """Sanitize a given type hint into a common parseable format.
        This is mostly to ensure that special types such as `None` whose name is `NoneType`
        can be handled by the library.

        :param type_hint: The type hint to sanitize.
        :type type_hint: str
        :return: The sanitized type hint.
        :rtype: str
        """

        def _get_context_frame() -> FrameInfo:
            for frame in stack():
                if frame.filename != __file__:
                    return frame

        _frame = _get_context_frame()
        if hasattr(typing, type_hint):
            if not isinstance(getattr(typing, type_hint), (_SpecialForm, TypeVar)):
                type_hint = getattr(typing, type_hint).__origin__.__name__
        elif type_hint in globals()["__builtins__"]:
            type_hint = globals()["__builtins__"][type_hint]
            if type_hint is None:
                type_hint = type(type_hint)

            type_hint = type_hint.__name__
        elif type_hint in _frame.frame.f_globals:
            type_hint = _frame.frame.f_globals[type_hint].__name__
        else:
            if type_hint != "_empty":
                LOGGER.warning(
                    "(doc-log) unknown type: `{!r}` provided, treating as literal.".format(
                        type_hint
                    )
                )

        return type_hint

    def _collect_sections(
        docstring: List[str],
        section_indexes: Dict[int, str],
        sections: Dict[str, SectionPattern],
    ) -> Dict[str, Section]:
        """Parse and collect all section items and define the name (if available) and the value of item.
        Then group all the items in their respective sections.

        :param docstring: The docstring to parse the section items from.
        :type docstring: List[str]
        :param section_indexes: The indexes defining where each item begins.
        :type section_indexes: Dict[int, str]
        :param sections: The sections that define each sections patterns.
        :type sections: Dict[str, SectionPattern]
        :return: The collected section items aggregated in their respective sections.
        :rtype: Dict[str, Section]
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
                SectionItem(value=value, name=name, _subitems=[])
            )

        LOGGER.debug(
            "(doc-log) parsed sections: `{!r}` from function: `{!s}` in `{!s}`".format(
                list(_collected_sections.keys()),
                _function.__name__,
                getmodule(_function).__file__,
            )
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
                _docstring.append(
                    ":{!s} {!s}".format(_section_indexes[index], docstring[_index])
                )
            indexes = indexes[1:]

        return _docstring

    def _parse_type_hints(_function: Callable) -> Tuple[Section, Section]:
        """Parse type hints from the function signature.

        :param _function: The function to extract the type hints from.
        :type _function: Callable
        :return: The type hints if the function is inspectable.
        :rtype: Tuple[Section, Section]
        """

        def _resolve_nested_type_hint(type_hint: Any, name: str = None) -> SectionItem:
            """Recursively unwrap a nested type hint into `SectionItem` types,
            with translated typing name.

            :param type_hint: Nested type hint.
            :type type_hint: Any
            :param name: Name of parameter, usually the name for the initial type, defaults to None
            :type name: str, optional
            :return: `SectionItem` containing the nested `SectionItem` types.
            :rtype: SectionItem
            """
            if hasattr(type_hint, "_name"):
                if type_hint._name is None:
                    # This is triggered when the type has no base type, i.e special types.
                    # Since we keep these we need to explicitly convert them in a similar fashion.
                    _start_index = str(type_hint).find(".")
                    _end_index = str(type_hint).find("[")

                    _item = SectionItem(
                        value=_sanitize_type_hint(
                            str(type_hint)[_start_index + 1 : _end_index]
                        ),
                        name=name,
                        _subitems=[],
                    )
                else:
                    _item = SectionItem(
                        value=_sanitize_type_hint(type_hint._name),
                        name=name,
                        _subitems=[],
                    )

                if hasattr(type_hint, "__args__"):
                    for argument in type_hint.__args__:
                        _item._subitems.append(_resolve_nested_type_hint(argument))
            else:
                if hasattr(type_hint, "__name__"):
                    return SectionItem(
                        value=_sanitize_type_hint(type_hint.__name__),
                        name=name,
                        _subitems=[],
                    )
                else:
                    return SectionItem(
                        value=_sanitize_type_hint(type(type_hint).__name__),
                        name=name,
                        _subitems=[],
                    )

            return _item

        _signature = signature(_function)

        return_types = Section(section="rtypes", items=[])
        if hasattr(_signature.return_annotation, "_name"):
            return_types.items.append(
                _resolve_nested_type_hint(_signature.return_annotation)
            )
        else:
            _type_hint = _signature.return_annotation
            return_types.items.append(
                SectionItem(
                    value=_sanitize_type_hint(
                        _type_hint.__name__
                        if hasattr(_type_hint, "__name__")
                        else _type_hint
                    ),
                    _subitems=[],
                )
            )

        parameters_types = Section(section="types", items=[])
        for parameter in _signature.parameters.values():
            if hasattr(parameter.annotation, "_name"):
                parameters_types.items.append(
                    _resolve_nested_type_hint(
                        type_hint=parameter.annotation, name=parameter.name
                    )
                )
            else:
                _type_hint = parameter.annotation
                parameters_types.items.append(
                    SectionItem(
                        value=_sanitize_type_hint(
                            _type_hint.__name__
                            if hasattr(_type_hint, "__name__")
                            else _type_hint
                        ),
                        name=parameter.name,
                        _subitems=[],
                    )
                )

        return parameters_types, return_types

    def _parse_type_hints_docstring(types: Section) -> Section:
        """Parse type hints from the function docstring and resolve them.

        :param types: Types defined in the docstring.
        :type types: Section
        :return: The type hints if the function is inspectable.
        :rtype: Section
        """

        def _resolve_type_hints(type_hint: str, name: str) -> SectionItem:
            """Recursively search through the type hint and extract each type and it's subitems.

            :param type_hint: The type hint to parse out items from.
            :type type_hint: str
            :param name: The name of the initial variable if applicable.
            :type name: str
            :return: The initial section item containing nested subitems if they exist.
            :rtype: SectionItem
            """
            _container_type = compile(r"[a-zA-Z0-9\_]*(?=\[)").search(type_hint)
            if _container_type is not None:
                _section_item = SectionItem(
                    value=_sanitize_type_hint(_container_type.group().strip()),
                    name=name,
                    _subitems=[],
                )

                _nested_types = compile(r"(?<=\[).*").search(type_hint)
                if _nested_types is not None and _nested_types.group().endswith("]"):
                    _nested_level, _start_index = 0, 0
                    for index, char in enumerate(_nested_types.group()[:-1] + ","):
                        if char == "," and _nested_level == 0:
                            _section_item._subitems.append(
                                _resolve_type_hints(
                                    type_hint=_nested_types.group()[:-1][
                                        _start_index:index
                                    ].strip(),
                                    name=None,
                                )
                            )
                            _start_index = index + 1
                        else:
                            if char == "[":
                                _nested_level += 1
                            elif char == "]":
                                _nested_level -= 1

                else:
                    LOGGER.warning(
                        "(doc-log) parameter: `{!s}` was a container type but no nested type was found, or it was otherwise malformed.".format(
                            name
                        )
                    )
            else:
                _section_item = SectionItem(
                    value=_sanitize_type_hint(type_hint), name=name, _subitems=[]
                )

            return _section_item

        _types = Section(section=types.section, items=[])
        for section_item in types.items:
            _types.items.append(
                _resolve_type_hints(section_item.value, section_item.name)
            )

        return _types

    def _parse_multiline(
        _function: Callable,
        sections: Dict[str, SectionPattern],
        _convert_to_oneline: Optional[Dict[str, Section]] = None,
    ) -> Union[Dict[str, Section], None]:
        """General multiline docstring parser. Takes an initial docstring and converts it given
        the specified syntax rules as defined by the sections. Optionally convert to oneline items if provided.

        :param _function: The called function that should be inspected for docstring and type hints.
        :type _function: Callable
        :param sections: The sections describing what sections there are and how to parse them.
        :type sections: Dict[str, SectionPattern]
        :param _convert_to_oneline: If the docstring contains multiline items then convert them given and parse using updated sections, defaults to None
        :type _convert_to_oneline: Optional[Dict[str, Section]], optional
        :return: The parsed docstring into their respective sections.
        :rtype: Union[Dict[str, Section], None]
        """
        if not _function.__doc__:
            LOGGER.error(
                "(doc-log) docstring was not found for function: `{!s}` in `{!s}`".format(
                    _function.__name__, getmodule(_function).__file__
                )
            )
            return None

        split_docstring = [
            line for line in _function.__doc__.split("\n") if line.strip()
        ]
        if _convert_to_oneline is not None:
            split_docstring = _convert_to_oneline_items(
                docstring=split_docstring, sections=sections
            )
            sections = _convert_to_oneline

        section_indexes = _parse_section_indexes(
            docstring=split_docstring, sections=sections
        )

        sections = _collect_sections(
            docstring=split_docstring,
            section_indexes=section_indexes,
            sections=sections,
        )

        if "types" in sections:
            sections["types"] = _parse_type_hints_docstring(types=sections["types"])

        if "rtypes" in sections:
            sections["rtypes"] = _parse_type_hints_docstring(types=sections["rtypes"])

        parsed_parameter_type_hints, parsed_return_type_hints = _parse_type_hints(
            _function=_function,
        )

        if parsed_parameter_type_hints:
            _parameter_type_hints = {
                section_item.name: section_item
                for section_item in parsed_parameter_type_hints.items
            }

            if "types" in sections:
                _parameter_type_hints_docstring = {
                    section.name: section for section in sections["types"].items
                }

                for parameter, section_item in _parameter_type_hints_docstring.items():
                    if str(_parameter_type_hints[parameter]) != str(section_item):
                        LOGGER.warning(
                            "(doc-log) parameter: `{!s}` had different type hints in the docstring and in the signature, signature: `{!s}` / docstring: `{!s}`".format(
                                parameter,
                                _parameter_type_hints[parameter],
                                section_item,
                            )
                        )
                        _parameter_type_hints[parameter] = section_item
            else:
                for parameter, section_item in _parameter_type_hints.items():
                    LOGGER.warning(
                        "(doc-log) parameter: `{!s}` had different type hints in the docstring and in the signature, signature: `{!s}` / docstring: `_empty`".format(
                            parameter,
                            _parameter_type_hints[parameter],
                        )
                    )

            sections["types"] = Section(
                section="types",
                items=[section_item for section_item in _parameter_type_hints.values()],
            )

        if parsed_return_type_hints:
            _return_type_hints = {
                section_item.name: section_item
                for section_item in parsed_return_type_hints.items
            }

            if "rtypes" in sections:
                _return_type_hints_docstring = {
                    section.name: section for section in sections["rtypes"].items
                }

                for parameter, section_item in _return_type_hints_docstring.items():
                    if str(_return_type_hints[parameter]) != str(section_item):
                        LOGGER.warning(
                            "(doc-log) return type had different type hints in the docstring and in the signature, signature: `{!s}` / docstring: `{!s}`".format(
                                _return_type_hints[parameter],
                                section_item,
                            )
                        )
                        _return_type_hints[parameter] = section_item
            else:
                for parameter, section_item in _return_type_hints.items():
                    LOGGER.warning(
                        "(doc-log) return type had different type hints in the docstring and in the signature, signature: `{!s}` / docstring: `_empty`".format(
                            _return_type_hints[parameter],
                        )
                    )

            sections["rtypes"] = Section(
                section="rtypes",
                items=[section_item for section_item in _return_type_hints.values()],
            )

        return sections

    # Most of the styles were taken from PEP257,
    # https://stackoverflow.com/questions/3898572/what-is-the-standard-python-docstring-format
    def _parse_pep257_multiline(_function: Callable) -> Dict[str, str]:
        """Parse docstring and extract rules from docstrings formatted by the
        multiline PEP257 standard.

        :param _function: The called function that should be inspected for docstring and type hints.
        :type _function: Callable
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
            _function=_function,
            sections=sections,
            _convert_to_oneline=sections_oneline,
        )

    def _parse_epytext_multiline(_function: Callable) -> Dict[str, str]:
        """Parse docstring and extract rules from docstrings formatted by the
        multiline Epytext standard.

        :param _function: The called function that should be inspected for docstring and type hints.
        :type _function: Callable
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
            _function=_function,
            sections=sections,
        )

    def _parse_rest_multiline(_function: Callable) -> Dict[str, str]:
        """Parse docstring and extract rules from docstrings formatted by the
        multiline reST standard.

        :param _function: The called function that should be inspected for docstring and type hints.
        :type _function: Callable
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
            _function=_function,
            sections=sections,
        )

    def _parse_google_multiline(_function: Callable) -> Dict[str, str]:
        """Parse docstring and extract rules from docstrings formatted by the
        multiline Google standard.

        :param _function: The called function that should be inspected for docstring and type hints.
        :type _function: Callable
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
            _function=_function,
            sections=sections,
            _convert_to_oneline=sections_oneline,
        )

    def _parse_numpydoc_multiline(_function: Callable) -> Dict[str, str]:
        """Parse docstring and extract rules from docstrings formatted by the
        multiline NumpyDoc standard.

        :param _function: The called function that should be inspected for docstring and type hints.
        :type _function: Callable
        :return: The rules extracted from the docstring.
        :rtype: Dict[str, str]
        """
        raise NotImplementedError

    if dialect.lower() == "pep257":
        return _parse_pep257_multiline(_function)
    elif dialect.lower() == "epytext":
        return _parse_epytext_multiline(_function)
    elif dialect.lower() == "rest":
        return _parse_rest_multiline(_function)
    elif dialect.lower() == "google":
        return _parse_google_multiline(_function)
    elif dialect.lower() == "numpydoc":
        return _parse_numpydoc_multiline(_function)
    else:
        raise ValueError(
            "dialect type: {!s}, expected one of `pep257`, `epytext`, `rest`, `google` or `numpydoc`".format(
                dialect
            )
        )
