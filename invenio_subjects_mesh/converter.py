# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Northwestern University.
#
# invenio-subjects-mesh is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""MeSH term converter."""


class MeSHConverter:
    """Convert MeSH term into subject dict for YAML writing."""

    def __init__(self, reader):
        """Constructor."""
        self._reader = reader

    def __iter__(self):
        """Iterate over converted entries."""
        for term in self._reader:
            yield {
                "id": term['UI'],
                "tags": ["mesh"],
                "title": {
                    "en": term['MH']
                }
            }
