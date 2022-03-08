# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2022 Northwestern University.
#
# invenio-subjects-mesh is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Download MeSH file."""

import shutil

import requests


class MeSHDownloader:
    """Download MeSH files."""

    def __init__(self, directory):
        """Constructor."""
        self.directory = directory
        self.topics_filepath = ""
        self.qaulifiers_filepath = ""
        self.base_url = "https://nlmpubs.nlm.nih.gov/projects/mesh/MESH_FILES/asciimesh/"  # noqa

    def download(self):
        """Download MeSH files of interest."""
        # topics
        self.topics_filepath = self.download_file(self.base_url + "d2022.bin")
        # qualifiers
        self.qualifiers_filepath = self.download_file(
            self.base_url + "q2022.bin"
        )

    def download_file(self, url):
        """Download a file."""
        filename = url.rsplit('/', 1)[-1]
        filepath = self.directory / filename

        with requests.get(url, stream=True) as req:
            with open(filepath, 'wb') as f:
                shutil.copyfileobj(req.raw, f)

        return filepath
