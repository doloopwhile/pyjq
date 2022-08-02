
Development
-----------

## Pipenv

This project uses [Pipenv](https://docs.pipenv.org/en/latest/) to manage dependencies.

Please install development tools with the following command:

```shell
pipenv install --dev
```

## Test

We can run the tests with `tox`.

```shell
pipenv run pytest --doctest-modules --ignore-glob='dependencies/**/*.py'
```

On pull request, Tox is executed in Circle CI.

## We DO commit `_pyjq.c`

When you edit `_pyjq.pyx`, you need to run `pipenv run cython _pyjq.pyx` before you run `pipenv run python setup.py develop`.
You need to do this because `setup.py` in this project does not compile `.pyx` to `.c` .

Of course, we can use `Cython.Build.cythonize` in `setup.py` to automatically compile `.pyx` to `.c` .
But, it causes a bootstrap problem in ``pip install``.

So, we DO commit both of `_pyjq.pyx` and `_pyjq.c`.

## Release

*This article is just for author. You don't have to do a release after PR.*

Edit CHANGELOG.md. Increment version in setup.cfg.

```shell
$ git commit -m "Version X.X.X" setup.cfg CHANGELOG.md
$ git push
```

Build.

```shell
$ pipenv --rm
$ pipenv install --dev
$ pipenv shell
$ rm -rf dist/
$ cython _pyjq.pyx
$ git status # check unexpected changes
$ python setup.py sdist --formats=gztar
$ python setup.py bdist_wheel
```

Release.

```shell
$ twine upload dist/*
```