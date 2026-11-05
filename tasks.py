#
# Copyright (C) 2023-2026 Northwestern University.
#
# invenio-subjects-mesh is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Makefile-like for Python project."""

from invoke import task


@task
def test(c, color=True, passthru=""):
    """Run tests."""
    c.run("ruff check", pty=color)
    c.run(f"python -m pytest {passthru}", pty=color)


@task
def clean(c):
    """Clean."""
    c.run("rm -rf *.egg-info/ */*.egg-info/ dist/ build/")
