#!/bin/bash
cat README.md \
  | grep -v -F '![Build Status]' \
  | pandoc -f commonmark -t rst - >| README.rst
