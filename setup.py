# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Northwestern University.
#
# invenio-subjects-mesh is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""MeSH subject terms for InvenioRDM"""

import os

from setuptools import find_packages, setup

readme = open('README.md').read()
history = open('CHANGES.md').read()

tests_require = [
    'pytest-invenio>=1.4.0',
]

dev_requires = [
    'click>=7.0',
    'pyyaml>=5.4.1',
    'requests>=2.25.1'
]

extras_require = {
    'docs': [
        'Sphinx>=3,<4',
    ],
    'tests': tests_require,
    'dev': dev_requires
}

extras_require['all'] = []
for reqs in extras_require.values():
    extras_require['all'].extend(reqs)

setup_requires = [
    'Babel>=2.8',
]

install_requires = []

packages = find_packages()


# Get the version string. Cannot be done with import!
g = {}
with open(os.path.join('invenio_subjects_mesh', 'version.py'), 'rt') as fp:
    exec(fp.read(), g)
    version = g['__version__']

setup(
    name='invenio-subjects-mesh',
    version=version,
    description=__doc__,
    long_description=readme + '\n\n' + history,
    long_description_content_type='text/markdown',
    keywords='invenio inveniordm subjects MeSH',
    license='MIT',
    author='Northwestern University',
    author_email='DL_FSM_GDS@e.northwestern.edu',
    url='https://github.com/galterlibrary/invenio-subjects-mesh',
    packages=packages,
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    entry_points={
        'console_scripts': [
            "invenio-subjects-mesh = invenio_subjects_mesh.cli:main"
        ],
        'invenio_rdm_records.fixtures': [
            'invenio_subjects_mesh = invenio_subjects_mesh.vocabularies',
        ],
    },
    extras_require=extras_require,
    install_requires=install_requires,
    setup_requires=setup_requires,
    tests_require=tests_require,
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
