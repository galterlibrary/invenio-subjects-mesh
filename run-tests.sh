#!/usr/bin/env bash
# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Northwestern University.
#
# invenio-subjects-mesh is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.


# Quit on errors
set -o errexit

# Quit on unbound symbols
set -o nounset

python -m check_manifest
python -m pytest
tests_exit_code=$?
exit "$tests_exit_code"
