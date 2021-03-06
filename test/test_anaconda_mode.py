from __future__ import (
    absolute_import, unicode_literals, division, print_function)
from os.path import abspath

import anaconda_mode


# Completion.


def test_completion_response():
    """Check completions works."""

    path = abspath('test.py')

    completions = anaconda_mode.complete('''
def test1(a, b):
    """First test function."""
    pass

def test2(c):
    """Second test function."""
    pass

test
''', 10, 4, path)

    assert completions == [{
        "name": "test1",
        "doc": 'test1(a, b)\n\nFirst test function.',
        'info': 'First test function.',
        'type': 'function',
        'path': path,
        'line': 2,
    }, {
        "name": "test2",
        "doc": 'test2(c)\n\nSecond test function.',
        'info': 'Second test function.',
        'type': 'function',
        'path': path,
        'line': 6,
    }]


# Definitions.


def test_goto_definitions():
    """Check goto definitions works."""

    path = abspath('test.py')

    definitions = anaconda_mode.goto_definitions('''
def fn(a, b):
    pass
fn(1, 2)
''', 4, 2, path)

    assert definitions == [{
        'line': 2,
        'column': 0,
        'name': 'fn',
        'description': 'def fn(a, b):',
        'module': 'test',
        'type': 'function',
        'path': path
    }]


def test_unknown_definition():
    """Check we process not found error."""

    definitions = anaconda_mode.goto_definitions('''
raise
''', 2, 5, None)

    assert not definitions


def test_goto_assignments():
    """Check goto assignments works."""

    assignments = anaconda_mode.goto_assignments('''
if a:      x = 1
else if b: x = 2
else if c: x = 3
else:      x = 4
    x
''', 6, 5, None)

    assert sorted(assign['line'] for assign in assignments) == [2, 3, 4, 5]


# Documentation.


def test_doc():
    """Check documentation lookup works."""

    doc = anaconda_mode.doc('''
def f(a, b=1):
    """Some docstring."""
    pass
''', 2, 4, 'some_module.py')

    assert doc == '''some_module - def f
========================================
f(a, b = 1)

Some docstring.'''


# Usages.


def test_usages():
    """Check usages search works."""

    usages = anaconda_mode.usages('''
import json
json.dumps
''', 3, 10, 'test.py')

    assert set(['test', 'json']) <= set(usage['module'] for usage in usages)


# ElDoc.


def test_eldoc():
    """Check eldoc on function with signature."""

    eldoc = anaconda_mode.eldoc('''
def f(obj, fp, skipkeys=False, ensure_ascii=True,
    check_circular=True, allow_nan=True, cls=None,
    indent=None, separators=None, default=None,
    sort_keys=False, **kw):
    pass

f(123
''', 8, 5, None)

    assert eldoc == {
        'name': 'f',
        'index': 0,
        'params': ['obj', 'fp', 'skipkeys = False', 'ensure_ascii = True',
                   'check_circular = True', 'allow_nan = True', 'cls = None',
                   'indent = None', 'separators = None', 'default = None',
                   'sort_keys = False', '**kw']
    }


def test_eldoc_unknown_function():
    """Check eldoc ignore unknown functions."""

    eldoc = anaconda_mode.eldoc('''
unknown_fn(
''', 2, 11, None)

    assert not eldoc
