# doc-log

`doc-log` offers the ability to parse docstrings and ultimately make decisions based on parsed rules. Everything that `doc-log` can do is listed under the [Features](#features) section. Follow the steps in [Setup](#setup) to install `doc-log`. Examples and use-cases are listed under the [Examples](#examples) section.

<a name="features"></a>

## Features

### Parsing

-   Parse docstrings based on any of the supported formats.
    -   [✔] `PEP257`
    -   [✔] `Epytext`
    -   [✔] `rEST`
    -   [✔] `Google`
    -   [ ] `numpydoc`

### Type Checking

-   Enforce runtime type checking based on the `function`/`method` docstring.
    -   [ ] `PEP257`
    -   [ ] `Epytext`
    -   [ ] `rEST`
    -   [ ] `Google`
    -   [ ] `numpydoc`

### Logging

-   Log `function`/`method` calls based on docstring.

    -   [ ] `PEP257`
    -   [ ] `Epytext`
    -   [ ] `rEST`
    -   [ ] `Google`
    -   [ ] `numpydoc`

-   Logging Information

    -   Debug

        -   [ ] Module that the `function`/`method` was called from.
        -   [ ] Time of `function`/`method` call.
        -   [ ] Passive type checking of passed parameters.
        -   [ ] Active type checking of passed parameters and return types.

    -   Info

        -   [ ] Module that the `function`/`method` was called from.
        -   [ ] Time of `function`/`method` call.

    -   Error

        -   [ ] Module that the `function`/`method` was called from.
        -   [ ] Time of `function`/`method` call.
        -   [ ] Active type checking of passed parameters and return types.

    -   Warning

        -   [ ] Module that the `function`/`method` was called from.
        -   [ ] Time of `function`/`method` call.
        -   [ ] Passive type checking of passed parameters and return types.

<a name="examples"></a>

## Examples

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
>>> python3 add_two.py
{'returns': Section(section='returns', items=[SectionItem(value='Integer `i` plus two (2)', name=None)]), 'arguments': Section(section='arguments', items=[SectionItem(value='the provided integer', name='i')])}
```

<a name="setup"></a>

## Setup

`doc-log` does not use any external dependency (except for [pytest](https://docs.pytest.org/en/latest/) and [black](https://black.readthedocs.io/en/stable/) when developing)

```
git clone https://github.com/wahl-sec/doc-log.git && cd doc-log && pip install .
```
