# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2022 Northwestern University.
#
# invenio-subjects-mesh is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Command line tool."""

from pathlib import Path

import click

from .converter import MeSHConverter
from .downloader import MeSHDownloader
from .reader import MeSHReader, topic_filter
from .writer import write_jsonl


@click.command()
@click.argument("year")
def main(**parameters):
    """Generate new subjects_mesh.jsonl file."""
    year = parameters["year"]

    downloads_dir = Path(__file__).parent / "downloads"
    files = MeSHDownloader(downloads_dir)
    files.download(year)

    topics_reader = MeSHReader(files.descriptors_filepath, filter=topic_filter)
    qualifiers_reader = MeSHReader(files.qualifiers_filepath)

    converter = MeSHConverter(topics_reader, qualifiers_reader)

    filepath = write_jsonl(converter)

    print(f"MeSH terms written here {filepath}")
