pyjq: Binding for jq JSON Processor
===================================

pyjq is a Python bindings for jq (http://stedolan.github.io/jq/).

    jq is like sed for JSON data – you can use it to slice and filter
    and map and transform structured data with the same ease that sed,
    awk, grep and friends let you play with text.

    http://stedolan.github.io/jq/

You can seamlessly call jq script (like regular expression) and process
plain python data structure.

For your information, https://pypi.python.org/pypi/jq is a also jq
bindings but different and incompatible with pyjq.

Example
-------

::

    >>> data = dict(
    ...     parameters= [
    ...         dict(name="PKG_TAG_NAME", value="trunk"),
    ...         dict(name="GIT_COMMIT", value="master"),
    ...         dict(name="TRIGGERED_JOB", value="trunk-buildall")
    ...     ],
    ...     id="2013-12-27_00-09-37",
    ...     changeSet=dict(items=[], kind="git"),
    ... )
    >>> import pyjq
    >>> pyjq.first('.parameters[] | {"param_name": .name, "param_type":.type}', data)
    {'param_type': None, 'param_name': 'PKG_TAG_NAME'}

Install
-------

You can install from PyPI by usual way.

::

    pip install pyjq

API
---

For jq script, `see its
manual <http://stedolan.github.io/jq/manual/>`__.

Only four APIs are provided. They are ``all``, ``one``, ``first``,
``compile``.

``all(script, value, **kw)``
    Transform object by jq script, returning all results as list.
    ``apply`` is an alias of ``all``

``first(script, value, default=None, **kw)``
    Transform object by jq script, returning the first result. Return
    default if result is empty.

``one(script, value, **kw)``
    Transform object by jq script, returning the first result. Raise
    ValueError unless results does not include exactly one element.

``compile(script, **kw)``
    Compile a jq script, retuning a script object.

Limitation
----------

jq is a JSON Processor. Therefore pyjq is able to process only "JSON
compatible" data (object made only from str, int, float, list, dict).

Q&A
---

How can I process json string got from API by pyjq?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You should apply ``json.loads`` in the standard library before pass to
pyjq.

License
-------

Copyright (c) 2014 OMOTO Kenji. Released under the MIT license. See
LICENSE for details.
