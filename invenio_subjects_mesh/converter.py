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

    def generate_id(self, identifier):
        """Generate URI id."""
        return f"https://id.nlm.nih.gov/mesh/{identifier}"

    def __iter__(self):
        """Iterate over converted entries."""
        for term in self._reader:
            yield {
                "id": self.generate_id(term['UI']),
                "scheme": "MeSH",
                "subject": term['MH']
            }
