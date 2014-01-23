import _pyjq
__all__ = []


def compile(script, **kw):
    """
    Compile a jq script, retuning a script object.
    """
    return _pyjq.Script(script.encode('utf-8'), kw)


def all(script, value, **kw):
    """
    Transform object by jq script, returning all results as list.
    """
    return compile(script, **kw).apply(value)

apply = all

def first(script, value, default=None, **kw):
    """
    Transform object by jq script, returning the first result.
    Return default if result is empty.
    """
    return compile(script, **kw).first(value, default)


def one(script, value, **kw):
    """
    Transform object by jq script, returning the first result.
    Raise ValueError unless results does not include exactly one element.
    """
    return compile(script, **kw).one(value)
