# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2023 Northwestern University.
#
# invenio-subjects-mesh is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Test subjects extension conforms to subjects extension interface."""

from pathlib import Path

import pkg_resources
import yaml

from invenio_subjects_mesh import __version__


def test_version():
    """Test version import."""
    assert __version__


def test_vocabularies_yaml():
    """Test vocabularies.yaml structure."""
    extensions = [
        ep.load() for ep in
        pkg_resources.iter_entry_points('invenio_rdm_records.fixtures')
    ]

    assert len(extensions) == 1

    module = extensions[0]
    directory = Path(module.__file__).parent
    filepath = directory / "vocabularies.yaml"

    with open(filepath) as f:
        data = yaml.safe_load(f)
        assert len(data) == 1
        assert data["subjects"]
        assert data["subjects"]["pid-type"]
        assert data["subjects"]["schemes"]

        # don't care about values, but rather structure
        schemes = data["subjects"]["schemes"]
        assert len(schemes) == 1
        assert "id" in schemes[0]
        assert "data-file" in schemes[0]
        assert "name" in schemes[0]
        assert "uri" in schemes[0]
