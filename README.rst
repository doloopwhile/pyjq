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

Only four APIs are provided:

-  ``all``
-  ``first``
-  ``one``
-  ``compile``

``all`` transforms a value by JSON script and returns all results as a
list.

::

    >>> value = {"user":"stedolan","titles":["JQ Primer", "More JQ"]}
    >>> pyjq.all('{user, title: .titles[]}', value)
    [{'user': 'stedolan', 'title': 'JQ Primer'}, {'user': 'stedolan', 'title': 'More JQ'}]

``all`` takes an optional argument ``vars``. ``vars`` is a dictonary of
predefined variables for ``script``. The values in ``vars`` are avaiable
in the ``script`` as a ``$key``. That is, ``vars`` works like ``--arg``
option and ``--argjson`` option of jq command.

::

    >>> pyjq.all('{user, title: .titles[]} | select(.title == $title)', value, vars={"title": "More JQ"})
    [{'user': 'stedolan', 'title': 'More JQ'}]

``all`` takes an optional argument ``url``. If ``url`` is given, the
subject of transformation is got from the ``url``.

::

    >> pyjq.all(".[] | .login", url="https://api.github.com/repos/stedolan/jq/contributors") # get all contributors of jq
    ['nicowilliams', 'stedolan', 'dtolnay', ...

Additionally, ``all`` takes an optional argument ``opener``. The default
``opener`` will simply download contents by ``urllib.request.urlopen``
and decode by ``json.decode``. However, you can customize this behavior
using custom ``opener``.

``first`` is almost some to ``all`` but it ``first`` returns the first
result of transformation.

::

    >>> value = {"user":"stedolan","titles":["JQ Primer", "More JQ"]}
    >>> pyjq.all('{user, title: .titles[]}', value)
    [{'user': 'stedolan', 'title': 'JQ Primer'}, {'user': 'stedolan', 'title': 'More JQ'}]

``first`` returns ``default`` when there are no results.

::

    >>> value = {"user":"stedolan","titles":["JQ Primer", "More JQ"]}
    >>> pyjq.first('.titles[] | select(test("e"))', value) # The first title which is contains "e"
    'JQ Primer'

``first`` returns the first result of transformation. It returns
``default`` when there are no results.

::

    >>> value = {"user":"stedolan","titles":["JQ Primer", "More JQ"]}
    >>> pyjq.first('.titles[] | select(test("T"))', value, "Third JS") # The first title which is contains "T"
    'Third JS'

``one`` do also returns the first result of transformation but raise
Exception if there are no results.

::

    >>> value = {"user":"stedolan","titles":["JQ Primer", "More JQ"]}
    >>> pyjq.one('.titles[] | select(test("T"))', value)
    IndexError: Result of jq is empty

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

Author
------

`OMOTO Kenji <https://github.com/doloopwhile>`__

License
-------

Released under the MIT license. See LICENSE for details.

Changes
-------

2.1.0
~~~~~

-  API's translate JS object not to ``dict`` but to
   ``collections.OrderedDict``.

2.0.0
~~~~~

-  Semantic versioning.
-  Bundle source codes of jq and oniguruma.
-  Supported Python 3.5.
-  Dropped support for Python 3.2.
-  Aeded ``all`` method.

1.0
~~~

-  First release.
