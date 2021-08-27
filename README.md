# doc-log

<div>
    <a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg" /></a>
    <a href="https://codecov.io/gh/wahl-sec/doc-log"><img src="https://codecov.io/gh/wahl-sec/doc-log/branch/main/graph/badge.svg?token=5WLSLYQFWP"/></a>
</div>

`doc-log` offers the ability to parse docstrings and ultimately make decisions based on parsed rules. Everything that `doc-log` can do is listed under the [Features](#features) section. Follow the steps in [Setup](#setup) to install `doc-log`. Examples and use-cases are listed under the [Examples](#examples) section.

<a name="features"></a>

## Features

### Parsing

-   Parse docstrings based on any of the supported formats.
    -   [x] `PEP257`
    -   [x] `Epytext`
    -   [x] `rEST`
    -   [x] `Google`
    -   [ ] `numpydoc`

### Type Checking

-   Enforce runtime type checking based on the `function`/`method` docstring. Supports almost all of the types offered by the standard library [typing](https://docs.python.org/3/library/typing.html).
    -   [x] `PEP257`
    -   [x] `Epytext`
    -   [x] `rEST`
    -   [x] `Google`
    -   [ ] `numpydoc`

### Logging

-   Log `function`/`method` calls based on docstring.

    -   [x] `PEP257`
    -   [x] `Epytext`
    -   [x] `rEST`
    -   [x] `Google`
    -   [ ] `numpydoc`

-   Logging Information
    -   [x] Module that the `function`/`method` was called from.
    -   [x] Time of `function`/`method` call.
    -   [x] Passive type checking of passed parameters.
        - `Warning` level or below.
    -   [x] Active type checking of passed parameters and return types.
        - `Error` level or above.

<a name="examples"></a>

## Examples
### Using `doc-log`

```python
# add_two.py

from doc_log import doc_log


@doc_log(dialect="pep257", type_check=True, _active_type_check=True)
def add_two(i):
    """Add two (2) to a provided integer and return.

    Arguments:
    i -- the provided integer

    Types:
    i -- int

    Returns:
    Integer `i` plus two (2)

    Return Type:
    int
    """
    return i + 2


print(f"{add_two(i=2)} == 4")
```

```shell
$ python3 add_two.py
WARNING :: 2021-08-27 19:33:45,415 :: (doc-log :: <module>:14:25) parameter: `i` had different type hints in the docstring and in the signature, signature: `_empty` / docstring: `int`
WARNING :: 2021-08-27 19:33:45,415 :: (doc-log :: <module>:20:25) return type had different type hints in the docstring and in the signature, signature: `_empty` / docstring: `int`
INFO :: 2021-08-27 19:33:45,415 :: (doc-log :: <module>:7:25) function: `add_two` called from `.../doc-log/add_two.py` at: `2021-08-27T19:33:45.415286`
4 == 4
```

### Invalid Type Provided

```python
# add_two.py

from doc_log import doc_log


@doc_log(dialect="pep257", type_check=True, _active_type_check=True)
def add_two(i):
    """Add two (2) to a provided integer and return.

    Arguments:
    i -- the provided integer

    Types:
    i -- int

    Returns:
    Integer `i` plus two (2)

    Return Type:
    int
    """
    return i + 2


print(f"{add_two(i='2')} == 4")
```

```shell
$ python3 add_two.py
WARNING :: 2021-08-27 19:34:14,417 :: (doc-log :: <module>:14:25) parameter: `i` had different type hints in the docstring and in the signature, signature: `_empty` / docstring: `int`
WARNING :: 2021-08-27 19:34:14,417 :: (doc-log :: <module>:20:25) return type had different type hints in the docstring and in the signature, signature: `_empty` / docstring: `int`
Traceback (most recent call last):
  File ".../doc-log/add_two.py", line 25, in <module>
    print(f"{add_two(i='2')} == 4")
  File ".../doc-log/doc_log/__init__.py", line 48, in wrapper
    raise TypeError(
TypeError: (doc-log :: <module>:14:25) parameter: `i` was not of expected type: `int` was actually `str`
```

### Invalid Type Defined

```python
# add_two.py

from doc_log import doc_log


@doc_log(dialect="pep257", type_check=True, _active_type_check=True)
def add_two(i):
    """Add two (2) to a provided integer and return.

    Arguments:
    i -- the provided integer

    Types:
    i -- str

    Returns:
    Integer `i` plus two (2)

    Return Type:
    int
    """
    return i + 2


print(f"{add_two(i=2)} == 4")
```

```shell
$ python3 add_two.py
WARNING :: 2021-08-27 19:34:39,279 :: (doc-log :: <module>:14:25) parameter: `i` had different type hints in the docstring and in the signature, signature: `_empty` / docstring: `str`
WARNING :: 2021-08-27 19:34:39,279 :: (doc-log :: <module>:20:25) return type had different type hints in the docstring and in the signature, signature: `_empty` / docstring: `int`
Traceback (most recent call last):
  File ".../doc-log/add_two.py", line 25, in <module>
    print(f"{add_two(i=2)} == 4")
  File ".../doc-log/doc_log/__init__.py", line 48, in wrapper
    raise TypeError(
TypeError: (doc-log :: <module>:14:25) parameter: `i` was not of expected type: `str` was actually `int`
```

### Logging With Type Check

```python
# add_two.py

from logging import INFO, getLogger, basicConfig

basicConfig(format="%(levelname)s :: %(asctime)s :: %(message)s", level=INFO)
logger = getLogger(__name__)

from doc_log import doc_log


@doc_log(dialect="pep257", type_check=True)
def add_two(i, j=None):
    """Add two (2) to a provided integer and return.

    Arguments:
    i -- the provided integer

    Types:
    i -- int

    Returns:
    Integer `i` plus two (2)

    Return Type:
    int
    """
    logger.info("parameter: `i` is {!s}".format(i))
    return i + 2


print(f"{add_two(i=2, j=3)} == 4")
```

```shell
$ python3 add_two.py
WARNING :: 2021-08-27 19:35:03,278 :: (doc-log :: <module>:19:31) parameter: `i` had different type hints in the docstring and in the signature, signature: `_empty` / docstring: `int`
WARNING :: 2021-08-27 19:35:03,279 :: (doc-log :: <module>:25:31) return type had different type hints in the docstring and in the signature, signature: `_empty` / docstring: `int`
WARNING :: 2021-08-27 19:35:03,292 :: (doc-log :: <module>:12:31) parameter: `j` was not of expected type: `_empty` was actually `int`
INFO :: 2021-08-27 19:35:03,293 :: (doc-log :: <module>:12:31) function: `add_two` called from `.../doc-log/add_two.py` at: `2021-08-27T19:35:03.292657`
INFO :: 2021-08-27 19:35:03,293 :: parameter: `i` is 2
4 == 4
```

### Logging With Type Check (Error)

```python
# add_two.py

from logging import ERROR, getLogger, basicConfig

basicConfig(format="%(levelname)s :: %(asctime)s :: %(message)s", level=ERROR)
logger = getLogger(__name__)

from doc_log import doc_log


@doc_log(dialect="pep257", type_check=True)
def add_two(i, j=None):
    """Add two (2) to a provided integer and return.

    Arguments:
    i -- the provided integer

    Types:
    i -- int

    Returns:
    Integer `i` plus two (2)

    Return Type:
    int
    """
    logger.info("parameter: `i` is {!s}".format(i))
    return i + 2


print(f"{add_two(i=2, j=3)} == 4")
```

```shell
$ python3 add_two.py
Traceback (most recent call last):
  File ".../doc-log/add_two.py", line 31, in <module>
    print(f"{add_two(i=2, j=3)} == 4")
  File ".../doc-log/doc_log/__init__.py", line 48, in wrapper
    raise TypeError(
TypeError: (doc-log :: <module>:12:31) parameter: `j` was not of expected type: `_empty` was actually `int`
```

### Logging With Type Check (Debug)

```python
# add_two.py

from logging import DEBUG, getLogger, basicConfig

basicConfig(format="%(levelname)s :: %(asctime)s :: %(message)s", level=DEBUG)
logger = getLogger(__name__)

from doc_log import doc_log


@doc_log(dialect="pep257", type_check=True)
def add_two(i, j=None):
    """Add two (2) to a provided integer and return.

    Arguments:
    i -- the provided integer

    Types:
    i -- int

    Returns:
    Integer `i` plus two (2)

    Return Type:
    int
    """
    logger.info("parameter: `i` is {!s}".format(i))
    return i + 2


print(f"{add_two(i=2, j=3)} == 4")
```

```shell
$ python3 add_two.py
DEBUG :: 2021-08-27 19:35:56,182 :: (doc-log :: <module>:12:31) parsing docstring with dialect: `pep257` from function: `add_two` in `.../doc-log/add_two.py`
DEBUG :: 2021-08-27 19:35:56,183 :: (doc-log :: <module>:12:31) parsed sections: `['arguments', 'types', 'returns', 'rtypes']` from function: `add_two` in `.../doc-log/add_two.py`
WARNING :: 2021-08-27 19:35:56,184 :: (doc-log :: <module>:19:31) parameter: `i` had different type hints in the docstring and in the signature, signature: `_empty` / docstring: `int`
WARNING :: 2021-08-27 19:35:56,184 :: (doc-log :: <module>:25:31) return type had different type hints in the docstring and in the signature, signature: `_empty` / docstring: `int`
DEBUG :: 2021-08-27 19:35:56,190 :: (doc-log :: <module>:19:31) item: `int` is not nested, type checking directly against value: `2`
DEBUG :: 2021-08-27 19:35:56,190 :: (doc-log :: <module>:12:31) item: `_empty` is not nested, type checking directly against value: `3`
DEBUG :: 2021-08-27 19:35:56,191 :: (doc-log :: <module>:18:31) type check arguments results was: `{'i': SectionItemTypeResult(item=SectionItem(value='int', _subitems=[], name='i', lineno=7), result=True, expected='int', actual='int', _subitems=[]), 'j': SectionItemTypeResult(item=SectionItem(value='_empty', _subitems=[], name='j', lineno=0), result=False, expected='_empty', actual='int', _subitems=[])}`
WARNING :: 2021-08-27 19:35:56,191 :: (doc-log :: <module>:12:31) parameter: `j` was not of expected type: `_empty` was actually `int`
INFO :: 2021-08-27 19:35:56,191 :: (doc-log :: <module>:12:31) function: `add_two` called from `.../doc-log/add_two.py` at: `2021-08-27T19:35:56.191936`
DEBUG :: 2021-08-27 19:35:56,191 :: (doc-log :: <module>:12:31) function: `add_two` was passed arguments: `()` and keyword arguments: `{'i': 2, 'j': 3}`
INFO :: 2021-08-27 19:35:56,191 :: parameter: `i` is 2
DEBUG :: 2021-08-27 19:35:56,196 :: (doc-log :: <module>:25:31) return type: `int` is not nested, type checking directly against value: `4`
DEBUG :: 2021-08-27 19:35:56,198 :: (doc-log :: <module>:24:31) type check return results was: `SectionItemTypeResult(item=SectionItem(value='int', _subitems=[], name=None, lineno=13), result=True, expected='int', actual='int', _subitems=[])`
4 == 4
```

### Logging Without Type Check

```python
# add_two.py

from logging import INFO, getLogger, basicConfig

basicConfig(format="%(levelname)s :: %(asctime)s :: %(message)s", level=INFO)
logger = getLogger(__name__)

from doc_log import doc_log


@doc_log(dialect="pep257", type_check=False)
def add_two(i, j=None):
    """Add two (2) to a provided integer and return.

    Arguments:
    i -- the provided integer

    Types:
    i -- int

    Returns:
    Integer `i` plus two (2)

    Return Type:
    int
    """
    logger.info("parameter: `i` is {!s}".format(i))
    return i + 2


print(f"{add_two(i=2, j=3)} == 4")
```

```shell
$ python3 add_two.py
WARNING :: 2021-08-27 19:36:16,881 :: (doc-log :: <module>:19:31) parameter: `i` had different type hints in the docstring and in the signature, signature: `_empty` / docstring: `int`
WARNING :: 2021-08-27 19:36:16,881 :: (doc-log :: <module>:25:31) return type had different type hints in the docstring and in the signature, signature: `_empty` / docstring: `int`
INFO :: 2021-08-27 19:36:16,886 :: parameter: `i` is 2
4 == 4
```

### Parsing `PEP257` Docstring

```python
# add_two.py

from doc_log.parser import parse_docstring

def add_two(i: int) -> int:
    """Add two (2) to a provided integer and return.

    Arguments:
    i -- the provided integer

    Returns:
    Integer `i` plus two (2)
    """
    return i + 2

print(parse_docstring(add_two, dialect="pep257"))
```

```shell
$ python3 add_two.py
WARNING :: 2021-08-27 19:36:35,514 :: (doc-log :: <module>:7:18) parameter: `i` had different type hints in the docstring and in the signature, signature: `int` / docstring: `_empty`
WARNING :: 2021-08-27 19:36:35,514 :: (doc-log :: <module>:7:18) return type had different type hints in the docstring and in the signature, signature: `int` / docstring: `_empty`
{'arguments': Section(section='arguments', items=[SectionItem(value='the provided integer', _subitems=[], name='i', lineno=4)], _function=<code object add_two at 0x000002C883AD45B0, file ".../doc-log/add_two.py", line 6>, lineno=3), 'returns': Section(section='returns', items=[SectionItem(value='Integer `i` plus two (2)', _subitems=[], name=None, lineno=7)], _function=<code object add_two at 0x000002C883AD45B0, file ".../doc-log/add_two.py", line 6>, lineno=6), 'types': Section(section='types', items=[SectionItem(value='int', _subitems=[], name='i', lineno=0)], _function=<code object add_two at 0x000002C883AD45B0, file ".../doc-log/add_two.py", line 6>, lineno=0), 'rtypes': Section(section='rtypes', items=[SectionItem(value='int', _subitems=[], name=None, lineno=0)], _function=<code object add_two at 0x000002C883AD45B0, file ".../doc-log/add_two.py", line 6>, lineno=0)}
```

### Parsing Type Hints in `PEP257` Docstring

```python
# add_two.py

from doc_log.parser import parse_docstring


def add_two(i):
    """Add two (2) to a provided integer and return.

    Arguments:
    i -- the provided integer

    Types:
    i -- int

    Returns:
    Integer `i` plus two (2)

    Return Type:
    int
    """
    return i + 2


print(parse_docstring(_function=add_two, dialect="pep257"))
```

```shell
$ python3 add_two.py
WARNING :: 2021-08-27 19:36:58,722 :: (doc-log :: <module>:14:24) parameter: `i` had different type hints in the docstring and in the signature, signature: `_empty` / docstring: `int`
WARNING :: 2021-08-27 19:36:58,722 :: (doc-log :: <module>:20:24) return type had different type hints in the docstring and in the signature, signature: `_empty` / docstring: `int`
{'arguments': Section(section='arguments', items=[SectionItem(value='the provided integer', _subitems=[], name='i', lineno=4)], _function=<code object add_two at 0x000001A0E25D45B0, file ".../doc-log/add_two.py", line 6>, lineno=3), 'types': Section(section='types', items=[SectionItem(value='int', _subitems=[], name='i', lineno=7)], _function=<code object add_two at 0x000001A0E25D45B0, file ".../doc-log/add_two.py", line 6>, lineno=6), 'returns': Section(section='returns', items=[SectionItem(value='Integer `i` plus two (2)', _subitems=[], name=None, lineno=10)], _function=<code object add_two at 0x000001A0E25D45B0, file ".../doc-log/add_two.py", line 6>, lineno=9), 'rtypes': Section(section='rtypes', items=[SectionItem(value='int', _subitems=[], name=None, lineno=13)], _function=<code object add_two at 0x000001A0E25D45B0, file ".../doc-log/add_two.py", line 6>, lineno=12)}
```

### Parse Type Check Results in `PEP257` Docstring

```python
# add_two.py

from doc_log.parser import parse_docstring
from doc_log.types import type_check_arguments, type_check_rtypes


def add_two(i):
    """Add two (2) to a provided integer and return the original and the result.

    Arguments:
    i -- the provided integer

    Types:
    i -- int

    Returns:
    Integer `i` plus two (2)

    Return Type:
    Tuple[int, int]
    """
    return (i, i + 2)


parameters = {"i": 2}
result = add_two(**parameters)
docstring = parse_docstring(_function=add_two, dialect="pep257")

print("Arguments ==============")
print(type_check_arguments(docstring["types"], parameters=parameters))
print("Return ==============")
print(repr(type_check_rtypes(docstring["rtypes"], results=result)))
```

```shell
$ python3 add_two.py
WARNING :: 2021-08-27 19:37:24,673 :: (doc-log :: <module>:15:27) parameter: `i` had different type hints in the docstring and in the signature, signature: `_empty` / docstring: `int`
WARNING :: 2021-08-27 19:37:24,673 :: (doc-log :: <module>:21:27) return type had different type hints in the docstring and in the signature, signature: `_empty` / docstring: `tuple[int, int]`
Arguments ==============
{'i': SectionItemTypeResult(item=SectionItem(value='int', _subitems=[], name='i', lineno=7), result=True, expected='int', actual='int', _subitems=[])}
Return ==============
SectionItemTypeResult(item=SectionItem(value='tuple', _subitems=[SectionItem(value='int', _subitems=[], name=None, lineno=13), SectionItem(value='int', _subitems=[], name=None, lineno=13)], name=None, lineno=13), result=True, expected='tuple', actual='tuple', _subitems=[SectionItemTypeResult(item=SectionItem(value='int', _subitems=[], name=None, lineno=13), result=True, expected='int', actual='int', _subitems=[]), SectionItemTypeResult(item=SectionItem(value='int', _subitems=[], name=None, lineno=13), result=True, expected='int', actual='int', _subitems=[])])
```

<a name="setup"></a>

## Setup

`doc-log` does not use any external dependency (except for [pytest](https://docs.pytest.org/en/latest/) and [black](https://black.readthedocs.io/en/stable/) when developing)

```
git clone https://github.com/wahl-sec/doc-log.git && cd doc-log && pip install .
```
