# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2022 Northwestern University.
#
# invenio-subjects-mesh is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""MeSH term converter."""


class MeSHConverter:
    """Convert MeSH term into subject dict."""

    def __init__(self, topics_reader, qualifiers_reader):
        """Constructor."""
        self._topics_reader = topics_reader
        self._qualifier_map = {
            q.get("QA"): q for q in qualifiers_reader
        }

    def generate_id(self, identifier):
        """Generate URI id."""
        return f"https://id.nlm.nih.gov/mesh/{identifier}"

    def __iter__(self):
        """Iterate over converted entries."""
        for term in self._topics_reader:
            yield {
                "id": self.generate_id(term['UI']),
                "scheme": "MeSH",
                "subject": term['MH']
            }

            for qid in term.get("AQ", []):
                qualifier = self._qualifier_map.get(qid)

                if not qualifier:
                    continue

                yield {
                    "id": self.generate_id(term['UI'] + qualifier['UI']),
                    "scheme": "MeSH",
                    "subject": term['MH'] + "/" + qualifier['SH']
                }
