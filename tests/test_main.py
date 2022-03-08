"""Test MeSH extractor."""

from collections import namedtuple
from contextlib import contextmanager
from pathlib import Path
from unittest import mock

import pytest
import yaml

from invenio_subjects_mesh.converter import MeSHConverter
from invenio_subjects_mesh.downloader import MeSHDownloader
from invenio_subjects_mesh.reader import MeSHReader
from invenio_subjects_mesh.writer import write_yaml


@pytest.fixture(scope="module")
def src_filepath():
    return Path(__file__).parent / "data" / "fake_d2022.bin"


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


@mock.patch('invenio_subjects_mesh.downloader.requests.get')
def test_downloader(patched_get):
    # patch requests.get to return files
    patched_get.side_effect = fake_request_context
    downloads_dir = Path(__file__).parent / "downloads"
    files = MeSHDownloader(directory=downloads_dir)

    files.download()

    patched_get.assert_called()
    assert downloads_dir / "d2022.bin" == files.topics_filepath
    assert downloads_dir / "q2022.bin" == files.qualifiers_filepath


def test_reader(src_filepath):
    reader = MeSHReader(src_filepath, filter='topics')

    topics = [t for t in reader]

    assert topics == [
        {
            'MH': 'Abnormalities, Multiple',
            'DC': '1',
            'UI': 'D000015'
        },
        {
            'MH': 'Seed Bank',
            'DC': '1',
            'UI': 'D000068098'
        },
        {
            'MH': 'Filariasis',
            'DC': '1',
            'UI': 'D005368'
        },
        {
            'MH': 'Congenital Abnormalities',
            'DC': '1',
            'UI': 'D000013'
        },
        {
            'MH': 'Abdominal Injuries',
            'DC': '1',
            'UI': 'D000007'
        },
        {
            'MH': 'Abdominal Neoplasms',
            'DC': '1',
            'UI': 'D000008'
        },
        {
            'MH': 'Abbreviations as Topic',
            'DC': '1',
            'UI': 'D000004'
        },
        {
            'MH': 'Abdomen',
            'DC': '1',
            'UI': 'D000005'
        }
    ]


def test_converter():
    mesh_topics = [{
        'MH': 'Filariasis',
        'DC': '1',
        'UI': 'D005368'
    }]
    converter = MeSHConverter(mesh_topics)

    objects = [o for o in converter]

    assert objects == [
        {
            "id": 'https://id.nlm.nih.gov/mesh/D005368',
            "scheme": "MeSH",
            "subject": "Filariasis"
        }
    ]


def test_write():
    filepath = Path(__file__).parent / "test_subjects.yaml"
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

    write_yaml(entries, filepath)

    with open(filepath) as f:
        read_entries = yaml.safe_load(f)
    assert entries == read_entries

    try:
        filepath.unlink()  # TODO: add missing_ok=True starting python 3.8+
    except FileNotFoundError:
        pass
