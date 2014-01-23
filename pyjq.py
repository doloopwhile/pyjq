import _pyjq
__all__ = []


def compile(script, vars={}):
    """
    Compile a jq script, retuning a script object.
    """
    return _pyjq.Script(script.encode('utf-8'), vars={})


def all(script, value, vars={}):
    """
    Transform object by jq script, returning all results as list.
    """
    return compile(script, vars).apply(value)

apply = all


def first(script, value, default=None, vars={}):
    """
    Transform object by jq script, returning the first result.
    Return default if result is empty.
    """
    return compile(script, vars).first(value, default)


def one(script, value, vars={}):
    """
    Transform object by jq script, returning the first result.
    Raise ValueError unless results does not include exactly one element.
    """
    return compile(script, vars).one(value)
