# invenio-subjects-mesh

*MeSH topical subject terms with qualifiers for InvenioRDM*

<a href="https://pypi.org/project/invenio-subjects-mesh/">
  <img src="https://img.shields.io/pypi/v/invenio-subjects-mesh.svg">
</a>

Install this extension to get Medical Subject Headings topics with qualifiers into your instance.

If you are looking for a smaller MeSH vocabulary without the qualifiers, use
[invenio-subjects-mesh-lite](https://github.com/galterlibrary/invenio-subjects-mesh-lite) instead.

> [!NOTE]
> Both extensions map the `MeSH` subject id, so you can only install one of them. However, they
> use the same pattern for subject ids, so you can switch from one to the other easily if your
> needs change in the future.


## Installation

From your instance directory:

```bash
pipenv install invenio-subjects-mesh
```

This will add it to your Pipfile.

## Versions

**From 2025.1.15.2 onwards**

This package follows the following format for versions: `YYYY.mm.dd.patch` where

- `YYYY.mm.dd` is the date of retrieval of the MeSH terms with `mm` and `dd` NOT being 0-prefixed.
- `patch` is the patch number (0-indexed) so that multiple releases can be done on the same day (bug/security fixes) and non-subject related releases can be done as well.

This follows [calendar versioning](https://calver.org/) (for year, month, and day) and adds a patch number at the end. The package is typically updated on a quarterly basis. The following are illustrative (fictitious) examples of how to understand the versioning of this distribution package:

| Last MeSH update included | patch number | version of this project |
| ------------------------- | ------------ | ----------------------- |
| 2025-06-31                | 2            | 2025.6.31.2             |
| 2025-12-01                | 0            | 2025.12.1.0             |

**Prior to 2025.1.15.2**

This repository follows [calendar versioning](https://calver.org/) for year and month. It does a "best effort" attempt at tracking the MeSH updates in an *up-to-and-including* version date manner. The following are illustrative cases of how to understand the versioning of this distribution package:

| Last MeSH update included | version of this project | date of release of this project |
| ------------------------- | ----------------------- | ------------------------------- |
| 2024-01-31                | 2024.1.X                | any time after 2024-01-31       |
| 2023-12-31                | 2023.12.X               | any time after 2023-12-31       |


`2021.06.18` is both a valid semantic version and an indicator of the year-month corresponding to the loaded terms.
`18` here is a patch number (not a day).

## Usage

There are 2 types of users for this package. Instance administrators and package maintainers.

### Instance operators

For instance operators, after you have installed the extension as per the steps above, you will want to reload your instance's fixtures: `pipenv run invenio rdm-records fixtures`. This will install the new terms in your instance.

Alternatively, or if you want to update your already loaded subjects to a new listing (e.g. from one year's list to another), you can update your instance's MeSH subjects as per below. Updating subjects this way takes care of everything for you: the subjects themselves and the records/drafts using those subjects. **WARNING** This operation can _remove_ subjects.

```bash
# In your instance's project
# Download up-to-date listings
pipenv run invenio galter_subjects mesh download -d /path/to/downloads/storage/ -y YEAR
# Generate file containg deltas to transition your instance to the downloaded listing
pipenv run invenio galter_subjects mesh deltas -d /path/to/downloads/storage/ -y YEAR -f topic-qualifier -o deltas_mesh.csv
# Update your instance - *this operation will modify your instance*
pipenv run invenio galter_subjects update deltas_mesh.csv
```

Look at the help text for these commands to see additional options that can be passed.
In particular, options for `galter_subjects update` allow you to store renamed, replaced or removed subjects on records according to a template of your choice.

### Maintainers

When a new list of MeSH term comes out, this package should be updated. Here we show how.

**Pre-requisite/Context**

[Install the distribution package for development](#development) before you do anything.

**Commands**

Once you have it installed, you can run the following commands in the isolated virtualenv:

```bash
# In this project
# Download up-to-date listings
(venv) invenio galter_subjects mesh download -d /path/to/downloads/storage/ -y YEAR
# Generate file containing initial listing
(venv) invenio galter_subjects mesh file -d /path/to/downloads/storage/ -y YEAR -f topic-qualifier -o invenio_subjects_mesh/vocabularies/subjects_mesh.csv
```

When you are happy with the list, bump the version in `pyproject.toml` and release it.

## Development

Install the project in editable mode with `dev` dependencies in an isolated virtualenv (`(venv)` denotes that going forward):

```bash
(venv) pip install -e .[dev]
# or if using pipenv
pipenv run pip install -e .[dev]
```

Run tests:

```bash
(venv) invoke test
# or shorter
(venv) inv test
# or if using pipenv
pipenv run inv test
```

Test compatibility with the pre-release version of InvenioRDM (invenio-app-rdm):

```bash
# Step 1 - install the pre-release dependencies
(venv) pip install --pre -e .[dev_pre]
# Step 2 - Run the pre-release tests
(venv) inv test
# if using uv run:
uv run --extra dev_pre --prerelease=allow inv test
```


Check manifest:

```bash
(venv) inv check-manifest
# or if using pipenv
pipenv run inv check-manifest
```

Clean out artefacts:

```bash
(venv) inv clean
# or if using pipenv
pipenv run inv clean
```
