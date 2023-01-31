#!/bin/sh -e
{%- if cookiecutter.auto_format == "y" %}
SRC=${1:-"pipelines steps run.py"}

set -x
# remove unused import statements and variables
autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place $SRC --exclude=__init__.py || true
# sorts imports
ruff $SRC --select I --fix --ignore D || true
# format code
black $SRC --exclude '' --include '\.pyi?$' -l 79 || true
{%- endif %}