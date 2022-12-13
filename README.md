# invenio-subjects-mesh

MeSH subject terms for InvenioRDM

Install this extension to get Medical Subject Headings topics into your instance.

## Installation

From your instance directory:

    pipenv install invenio-subjects-mesh

This will add it to your Pipfile.

### Versions

This repository follows [calendar versioning](https://calver.org/):

`2021.06.18` is both a valid semantic version and an indicator of the year-month corresponding to the loaded MeSH terms.


## Usage

There are 2 types of users for this package. Maintainers of the package and instance administrators.

### Instance administrators

For instance administrators, after you have installed the extension as per the steps above, you will want to reload your instance's fixtures: `pipenv run invenio rdm-records fixtures` . Updating existing terms currently requires manual replacement.

### Maintainers

When a new list of MeSH term comes out, this package should be updated. Here we show how.

0- Make sure you have cloned this package and installed it locally with the `all` extra:

    pipenv run pip install -e .[all]

1- Update:

    pipenv run invenio-subjects-mesh

   This will

   1- Download the new list (TODO - For now download it manually and place it in `invenio_subjects_mesh/download/data/`)
   2- Read it filtering for topics
   3- Convert terms to InvenioRDM subjects format
   4- Write those to `invenio_subjects_mesh/vocabularies/subjects_mesh.jsonl` file

2- When you are happy with the list, bump the version in `invenio_subjects_mesh/__init__.py` and release it.

**Note**

There are some amenities in the code to filter/interact with MeSH terms a little if one is so inclined.


## Future Ideas

- InvenioRDM doesn't have a way to update pre-existing subjects yet. Once there is one,
  this package should provide the functionality to update MeSH terms.
