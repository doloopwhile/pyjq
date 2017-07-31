import json
import re

from six.moves import urllib

import _pyjq

__all__ = []


def compile(script, vars={}, library_paths=None):
    """
    Compile a jq script, retuning a script object.

    library_paths is an array of strings that defines the module
    search path.  Semantics for these paths are the same as if
    provided to the jq command-line program's -L switch except that ~
    and $ORIGIN are not expanded.  If not provided, JQ's default list
    will be used.
    """

    return _pyjq.Script(script.encode('utf-8'), vars=vars,
                        library_paths=library_paths)


def default_opener(url):
    """
    """
    res = urllib.request.urlopen(url)
    content_type = res.getheader('Content-Type')

    if content_type is None:
        encoding = 'utf-8'
    else:
        m = re.search(r'charset\s*=\s*(\S+)', content_type, re.I)
        if m is None:
            encoding = 'utf-8'
        else:
            encoding = m.group(1)
    return json.loads(res.read().decode(encoding))


def _get_value(value, url, opener):
    if url is not None:
        if value is not None:
            raise TypeError("'value' and 'url' are not able to specified at the same time")
        return opener(url)
    return value


def all(script, value=None, vars={}, url=None, opener=default_opener, library_paths=None):
    """
    Transform value by script, returning all results as list.
    """
    return compile(script, vars, library_paths).all(_get_value(value, url, opener))


def apply(script, value=None, vars={}, url=None, opener=default_opener, library_paths=None):
    """
    Transform value by script, returning all results as list.
    """
    return all(script, value, vars, url, opener, library_paths)

apply.__doc__ = all.__doc__


def first(script, value=None, default=None, vars={}, url=None, opener=default_opener, library_paths=None):
    """
    Transform object by jq script, returning the first result.
    Return default if result is empty.
    """
    return compile(script, vars, library_paths).first(_get_value(value, url, opener), default)


def one(script, value=None, vars={}, url=None, opener=default_opener, library_paths=None):
    """
    Transform object by jq script, returning the first result.
    Raise ValueError unless results does not include exactly one element.
    """
    return compile(script, vars, library_paths).one(_get_value(value, url, opener))
