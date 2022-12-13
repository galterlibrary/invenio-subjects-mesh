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
        self.descriptors_filepath = ""
        self.qualifiers_filepath = ""
        self.base_url = "https://nlmpubs.nlm.nih.gov/projects/mesh/MESH_FILES/asciimesh/"  # noqa

    def download(self, year):
        """Download MeSH files of interest.

        :param year: str. year of the files to download.
        """
        # descriptors
        self.descriptors_filepath = self.download_file(
            self.base_url + f"d{year}.bin"
        )
        # qualifiers
        self.qualifiers_filepath = self.download_file(
            self.base_url + f"q{year}.bin"
        )

    def download_file(self, url):
        """Download a file."""
        filename = url.rsplit('/', 1)[-1]
        filepath = self.directory / filename

        with requests.get(url, stream=True) as req:
            with open(filepath, 'wb') as f:
                shutil.copyfileobj(req.raw, f)

        return filepath
