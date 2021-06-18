# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Northwestern University.
#
# invenio-subjects-mesh is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

# TODO: Place this file in download/ subpkg

"""Download MeSH file."""

import requests


def download_terms(url):
    """Download MeSH file."""
    requests.get(url)
    # store in download/data/
