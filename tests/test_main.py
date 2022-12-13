# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2022 Northwestern University.
#
# invenio-subjects-mesh is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Test MeSH extractor."""

from collections import namedtuple
from contextlib import contextmanager
from pathlib import Path
from unittest import mock

from invenio_subjects_mesh.converter import MeSHConverter
from invenio_subjects_mesh.downloader import MeSHDownloader
from invenio_subjects_mesh.reader import MeSHReader, read_jsonl, topic_filter
from invenio_subjects_mesh.writer import write_jsonl

# Helpers


@contextmanager
def fake_request_context(url, stream):
    fp = ""
    base_url = (
        "https://nlmpubs.nlm.nih.gov/projects/mesh/MESH_FILES/asciimesh/"
    )
    if url == base_url + "d2022.bin":
        fp = Path(__file__).parent / "data/fake_d2022.bin"
    elif url == base_url + "q2022.bin":
        fp = Path(__file__).parent / "data/fake_q2022.bin"
    else:
        raise Exception("Update the test!")

    FakeRequestContext = namedtuple("FakeRequestContext", ["raw"])

    with open(fp, "rb") as f:
        yield FakeRequestContext(raw=f)


def assert_includes(dicts, dict_cores):
    """Checks that each dict in dicts has the corresponding dict_core."""
    for d, dc in zip(dicts, dict_cores):
        for key, value in dc.items():
            assert value == d[key]


# Tests


@mock.patch('invenio_subjects_mesh.downloader.requests.get')
def test_downloader(patched_get):
    # patch requests.get to return files
    patched_get.side_effect = fake_request_context
    downloads_dir = Path(__file__).parent / "downloads"
    files = MeSHDownloader(directory=downloads_dir)
    year = "2022"

    files.download(year)

    patched_get.assert_called()
    assert downloads_dir / "d2022.bin" == files.descriptors_filepath
    assert downloads_dir / "q2022.bin" == files.qualifiers_filepath


def test_topics_reader():
    filepath = Path(__file__).parent / "data" / "fake_d2022.bin"
    reader = MeSHReader(filepath, filter=topic_filter)

    topics = [t for t in reader]

    expected_cores = [
        {
            'MH': 'Seed Bank',
            'DC': '1',
            'AQ': ['CL', 'EC'],
            'UI': 'D000068098'
        },
        {
            'MH': 'Abbreviations as Topic',
            'DC': '1',
            'UI': 'D000004'
        },
        {
            'MH': 'Abdomen',
            'DC': '1',
            'AQ': ['AB', 'AH'],
            'UI': 'D000005'
        }
    ]
    assert_includes(topics, expected_cores)


def test_qualifiers_reader():
    filepath = Path(__file__).parent / "data" / "fake_q2022.bin"
    reader = MeSHReader(filepath)

    qualifiers = [t for t in reader]

    expected_cores = [
        {
            "QA": "AB",
            "SH": "abnormalities",
            "UI": "Q000002"
        },
        {
            "QA": "AH",
            "SH": "anatomy & histology",
            "UI": "Q000033"
        },
        {
            "QA": "CL",
            "SH": "classification",
            "UI": "Q000145"
        },
        {
            "QA": "EC",
            "SH": "economics",
            "UI": "Q000191"
        },
    ]
    assert_includes(qualifiers, expected_cores)


def test_converter():
    mesh_topics = [{
        'MH': 'Seed Bank',
        'DC': '1',
        'AQ': ['CL', 'EC'],
        'UI': 'D000068098'
    }]
    mesh_qualifiers = [
        {
            "QA": "CL",
            "SH": "classification",
            "UI": "Q000145"
        },
        {
            "QA": "EC",
            "SH": "economics",
            "UI": "Q000191"
        },
    ]
    converter = MeSHConverter(mesh_topics, mesh_qualifiers)

    objects = [o for o in converter]

    assert objects == [
        {
            "id": 'https://id.nlm.nih.gov/mesh/D000068098',
            "scheme": "MeSH",
            "subject": "Seed Bank"
        },
        {
            "id": 'https://id.nlm.nih.gov/mesh/D000068098Q000145',
            "scheme": "MeSH",
            "subject": "Seed Bank/classification"
        },
        {
            "id": 'https://id.nlm.nih.gov/mesh/D000068098Q000191',
            "scheme": "MeSH",
            "subject": "Seed Bank/economics"
        },
    ]


def test_write():
    filepath = Path(__file__).parent / "test_subjects.jsonl"
    entries = [
        {
            "id": 'D000015',
            "tags": ["mesh"],
            "title": {
                "en": 'Abnormalities, Multiple'
            }
        },
        {
            "id": 'D000068098',
            "tags": ["mesh"],
            "title": {
                "en": 'Seed Bank'
            }
        },
        {
            "id": 'D005368',
            "tags": ["mesh"],
            "title": {
                "en": 'Filariasis'
            }
        }
    ]

    write_jsonl(entries, filepath)

    read_entries = list(read_jsonl(filepath))
    assert entries == read_entries

    try:
        filepath.unlink()  # TODO: add missing_ok=True starting python 3.8+
    except FileNotFoundError:
        pass
