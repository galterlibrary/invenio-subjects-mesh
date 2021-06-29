"""Test MeSH extractor."""

from pathlib import Path

import pytest
import yaml

from invenio_subjects_mesh.converter import MeSHConverter
from invenio_subjects_mesh.reader import MeSHReader
from invenio_subjects_mesh.writer import write_yaml


@pytest.fixture(scope="module")
def src_filepath():
    return Path(__file__).parent / "descriptors_test_file.bin"


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
            "id": 'D005368',
            "tags": ["mesh"],
            "title": {
                "en": 'Filariasis'
            }
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
