# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Northwestern University.
#
# invenio-subjects-mesh is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Command line tool."""

from pathlib import Path

import click

from .converter import MeSHConverter
from .download import download_terms
from .reader import MeSHReader
from .writer import write_yaml


@click.command()
def main():
    """Generate new subjects_mesh.yaml file."""
    # TODO: fetch via URL filepath = download_terms(url)
    # local for now
    filepath = Path(__file__).parent / "download/data/d2021.bin"

    reader = MeSHReader(filepath, filter='topics')

    converter = MeSHConverter(reader)

    filepath = write_yaml(converter)

    print(f"MeSH terms written here {filepath}")
