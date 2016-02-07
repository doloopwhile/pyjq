import json
import re

from six.moves import urllib

import _pyjq

__all__ = []


def compile(script, vars={}):
    """
    Compile a jq script, retuning a script object.
    """
    return _pyjq.Script(script.encode('utf-8'), vars=vars)


def _opener(url):
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

    return res.read().decode(encoding)


def _get_value(value, url, opener):
    if url is not None:
        if value is not None:
            raise TypeError("'value' and 'url' are not able to specified at the same time")
        if opener is None:
            opener = _opener
        return json.loads(opener(url))
    return value


def ensure_kwargs_empty(kw):
    if kw:
        raise TypeError('Got unexpected keyward argument {}'.format(', '.join(kw)))


def all(script, value=None, **kw):
    """
    Transform object by jq script, returning all results as list.
    """
    url = kw.pop('url', None)
    vars = kw.pop('vars', {})
    opener = kw.pop('opener', None)
    ensure_kwargs_empty(kw)

    return compile(script, vars).all(_get_value(value, url, opener))

apply = all


def first(script, value=None, default=None, **kw):
    """
    Transform object by jq script, returning the first result.
    Return default if result is empty.
    """
    url = kw.pop('url', None)
    vars = kw.pop('vars', {})
    opener = kw.pop('opener', None)
    ensure_kwargs_empty(kw)

    return compile(script, vars).first(_get_value(value, url, opener), default)


def one(script, value=None, **kw):
    """
    Transform object by jq script, returning the first result.
    Raise ValueError unless results does not include exactly one element.
    """
    url = kw.pop('url', None)
    vars = kw.pop('vars', {})
    opener = kw.pop('opener', None)
    ensure_kwargs_empty(kw)

    return compile(script, vars).one(_get_value(value, url, opener))
