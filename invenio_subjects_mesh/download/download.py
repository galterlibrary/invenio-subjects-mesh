# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Northwestern University.
#
# invenio-subjects-mesh is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Download MeSH file."""

import shutil
from pathlib import Path

import requests


def download_mesh():
    """Download MeSH file."""
    # 2021 ASCII MeSH terms
    url = "https://nlmpubs.nlm.nih.gov/projects/mesh/MESH_FILES/asciimesh/d2021.bin"  # noqa
    filename = url.rsplit('/', 1)[-1]
    filepath = Path(__file__).parent / filename

    with requests.get(url, stream=True) as req:
        with open(filepath, 'wb') as f:
            shutil.copyfileobj(req.raw, f)

    return filepath
