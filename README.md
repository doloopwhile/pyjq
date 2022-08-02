pyjq: Binding for jq JSON Processor
===================================

[![CircleCI](https://circleci.com/gh/doloopwhile/pyjq.svg?style=svg)](https://circleci.com/gh/doloopwhile/pyjq)

pyjq is a Python bindings for jq (<http://stedolan.github.io/jq/>).

> jq is like sed for JSON data - you can use it to slice and filter and
> map and transform structured data with the same ease that sed, awk,
> grep and friends let you play with text.
>
> <http://stedolan.github.io/jq/>

You can seamlessly call jq script (like regular expression) and process
a plain python data structure.

For your information, <https://pypi.python.org/pypi/jq> is another jq
binding which is different and incompatible with pyjq.

Example
-------

```python
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
{'param_name': 'PKG_TAG_NAME', 'param_type': None}

```

Install
-------

You will need flex, bison (3.0 or newer), libtool, make, automake and autoconf to build jq.
Install them by Homebrew, APT or other way.

You can install from PyPI by usual way.

```shell
pip install pyjq
```

API
---

For jq script, [see its manual](http://stedolan.github.io/jq/manual/).

Only four APIs are provided:

- `all`
- `first`
- `one`
- `compile`

`all` transforms a value by JSON script and returns all results as a list.

```python
>>> value = {"user":"stedolan","titles":["JQ Primer", "More JQ"]}
>>> pyjq.all('{user, title: .titles[]}', value)
[{'user': 'stedolan', 'title': 'JQ Primer'}, {'user': 'stedolan', 'title': 'More JQ'}]
```

`all` takes an optional argument `vars`.
`vars` is a dictonary of predefined variables for `script`.
The values in `vars` are available in the `script` as a `$key`.
That is, `vars` works like `--arg` option and `--argjson` option of jq command.

```python
>>> pyjq.all('{user, title: .titles[]} | select(.title == $title)', value, vars={"title": "More JQ"})
[{'user': 'stedolan', 'title': 'More JQ'}]
```

`all` takes an optional argument `url`.
If `url` is given, the subject of transformation is retrieved from the `url`.

```python
>> pyjq.all(".[] | .login", url="https://api.github.com/repos/stedolan/jq/contributors") # get all contributors of jq
['nicowilliams', 'stedolan', 'dtolnay', ... ]
```

Additionally, `all` takes an optional argument `opener`.
The default `opener` will download contents using `urllib.request.urlopen` and decode using `json.decode`.
However, you can customize this behavior using a custom `opener`.

`first` and `one` are similar to to `all`.

`first` returns the first result of transformation.
When there are no results, `first` returns `None` or the given `default`.

```python
>>> data = {"user":"stedolan","titles":["JQ Primer", "More JQ"]}
>>> pyjq.first('{user, title: .titles[]}', data)
{'user': 'stedolan', 'title': 'JQ Primer'}
>>> pyjq.first('.titles[] | select(test("T"))', data) # returns None
>>> pyjq.first('.titles[] | select(test("T"))', data, default="Third JS")
'Third JS'
```

`one` returns the only result of a transformation.
It raises an exception when there are no results or when there are two or more results.

```python
>>> data = {"user":"stedolan","titles": ["JQ Primer", "More JQ"]}
>>> pyjq.one('.titles[] | select(test("P"))', data)
'JQ Primer'
>>> pyjq.one('.titles[] | select(test("T"))', data)
Traceback (most recent call last):
IndexError: Result of jq is empty
>>> pyjq.one('.titles[] | select(test("J"))', data)
Traceback (most recent call last):
IndexError: Result of jq have multiple elements
```

`compile` is similar to `re.compile`. It accepts jq script and returns an object with methods.

```python
>>> data = {"user":"stedolan","titles":["JQ Primer", "More JQ"]}
>>> import pyjq
>>> pat = pyjq.compile('{user, title: .titles[]}')
>>> pat.all(data)
[{'user': 'stedolan', 'title': 'JQ Primer'}, {'user': 'stedolan', 'title': 'More JQ'}]
```

Limitations
-----------

jq is a JSON Processor. Therefore pyjq is able to process only
"JSON compatible" data (object made only from str, int, float, list, dict).

Q&A
---

### How can I process a json string (f.e. gotten from an API) with pyjq?

You should call `json.loads` from the standard library on the string, before you pass it to pyjq.

Author
------
[OMOTO Kenji](https://github.com/doloopwhile)

License
-------
MIT License. See [LICENSE](./LICENSE).

This package includes [jq](https://github.com/stedolan/jq) and [oniguruma](https://github.com/kkos/oniguruma). Their license files are included in their respective archive files.

- jq: `dependencies/jq-1.5.tar.gz`
- oniguruma: `dependencies/onig-6.9.0.tar.gz`
