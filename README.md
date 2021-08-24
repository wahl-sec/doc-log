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

-   Enforce runtime type checking based on the `function`/`method` docstring.
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
    -   [ ] Module that the `function`/`method` was called from.
    -   [ ] Time of `function`/`method` call.
    -   [ ] Passive type checking of passed parameters.
        - `Warning` level or below.
    -   [ ] Active type checking of passed parameters and return types.
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
Traceback (most recent call last):
  File ".../doc-log/add_two.py", line 25, in <module>
    print(f"{add_two(i='2')} == 4")
  File ".../doc-log/doc_log/__init__.py", line 29, in wrapper
    raise TypeError(
TypeError: `i` was not of expected type: `int` was actually `str`
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
Traceback (most recent call last):
  File ".../doc-log/add_two.py", line 25, in <module>
    print(f"{add_two(i='2')} == 4")
  File ".../doc-log/doc_log/__init__.py", line 29, in wrapper
    raise TypeError(
TypeError: `i` was not of expected type: `str` was actually `int`
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
WARNING :: 2021-08-24 10:05:18,409 :: (doc-log) parameter: `i` was type hinted in docstring but not in signature.
WARNING :: 2021-08-24 10:05:18,409 :: (doc-log) return type was type hinted in docstring: `int` but not in signature.
WARNING :: 2021-08-24 10:05:18,412 :: (doc-log) parameters that were not type hinted was passed, consumed: `i`, passed: `i, j`
WARNING :: 2021-08-24 10:05:18,412 :: (doc-log) parameter: `j` was not of expected type: `typing.Any` was actually `None`
INFO :: 2021-08-24 10:05:18,412 :: (doc-log) function: `add_two` called from `.../doc-log/add_two.py` at: `2021-08-24T10:05:18.412107`
INFO :: 2021-08-24 10:05:18,412 :: parameter: `i` is 2
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
  File ".../doc-log/add_two.py", line 33, in <module>
    print(f"{add_two(i=2, j=3)} == 4")
  File ".../doc-log/doc_log/__init__.py", line 45, in wrapper
    raise TypeError(
TypeError: `(doc-log) parameter: j` was not of expected type: `typing.Any` was actually `None`
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
DEBUG :: 2021-08-24 10:08:51,123 :: (doc-log) parsing docstring with dialect: `pep257` from function: `add_two` in `.../doc-log/add_two.py`
DEBUG :: 2021-08-24 10:08:51,128 :: (doc-log) parsed sections: `['rtypes', 'types', 'returns', 'arguments']` from function: `add_two` in `.../doc-log/add_two.py`
WARNING :: 2021-08-24 10:08:51,130 :: (doc-log) parameter: `i` was type hinted in docstring but not in signature.
WARNING :: 2021-08-24 10:08:51,130 :: (doc-log) return type was type hinted in docstring: `int` but not in signature.
DEBUG :: 2021-08-24 10:08:51,130 :: (doc-log) item: `int` is not nested, type checking directly against value: `2`
WARNING :: 2021-08-24 10:08:51,130 :: (doc-log) parameters that were not type hinted was passed, consumed: `i`, passed: `i, j`
WARNING :: 2021-08-24 10:08:51,131 :: (doc-log) parameter: `j` was not of expected type: `typing.Any` was actually `None`
INFO :: 2021-08-24 10:08:51,131 :: (doc-log) function: `add_two` called from `.../doc-log/add_two.py` at: `2021-08-24T10:08:51.131467`
DEBUG :: 2021-08-24 10:08:51,131 :: (doc-log) function: `add_two` was passed arguments: `()` and keyword arguments: `{'i': 2, 'j': 3}`
INFO :: 2021-08-24 10:08:51,131 :: parameter: `i` is 2
DEBUG :: 2021-08-24 10:08:51,131 :: (doc-log) return type: `int` is not nested, type checking directly against value: `4`
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
WARNING :: 2021-08-24 10:10:54,760 :: (doc-log) parameter: `i` was type hinted in docstring but not in signature.
WARNING :: 2021-08-24 10:10:54,760 :: (doc-log) return type was type hinted in docstring: `int` but not in signature.
INFO :: 2021-08-24 10:10:54,761 :: parameter: `i` is 2
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

print(parse_docstring(add_two.__doc__, dialect="pep257"))
```

```shell
$ python3 add_two.py
{'arguments': Section(section='arguments', items=[SectionItem(value='the provided integer', _subitems=[], name='i')]), 'returns': Section(section='returns', items=[SectionItem(value='Integer `i` plus two (2)', _subitems=[], name=None)]), 'types': Section(section='types', items=[SectionItem(value='int', _subitems=[], name='i')]), 'rtypes': Section(section='rtypes', items=[SectionItem(value='int', _subitems=[], name=None)])}
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
{'returns': Section(section='returns', items=[SectionItem(value='Integer `i` plus two (2)', _subitems=[], name=None)]), 'rtypes': Section(section='rtypes', items=[SectionItem(value='int', _subitems=[], name=None)]), 'arguments': Section(section='arguments', items=[SectionItem(value='the provided integer', _subitems=[], name='i')]), 'types': Section(section='types', items=[SectionItem(value='int', _subitems=[], name='i')])}
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
print(type_check_rtypes(docstring["rtypes"], results=result))
```

```shell
$ python3 add_two.py
Arguments ==============
{'i': SectionItemTypeResult(item=SectionItem(value='int', _subitems=[], name='i'), result=True, expected='int', actual='int', _subitems=[])}
Return ==============
[SectionItemTypeResult(item=SectionItem(value='tuple', _subitems=[SectionItem(value='int', _subitems=[], name=None), SectionItem(value='int', _subitems=[], name=None)], name=None), result=True, expected='tuple', actual='tuple', _subitems=[SectionItemTypeResult(item=SectionItem(value='int', _subitems=[], name=None), result=True, expected='int', actual='int', _subitems=[]), SectionItemTypeResult(item=SectionItem(value='int', _subitems=[], name=None), result=True, expected='int', actual='int', _subitems=[])])]
```

<a name="setup"></a>

## Setup

`doc-log` does not use any external dependency (except for [pytest](https://docs.pytest.org/en/latest/) and [black](https://black.readthedocs.io/en/stable/) when developing)

```
git clone https://github.com/wahl-sec/doc-log.git && cd doc-log && pip install .
```
