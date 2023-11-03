# Copyright (C) 2023 Northwestern University.
#
# invenio-subjects-mesh-lite is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

from invoke import task


@task
def test(c, color=True, passthru=""):
    """Run tests."""
    c.run(f"python -m pytest {passthru}", pty=color)


@task
def check_manifest(c, passthru=""):
    """Check manifest."""
    c.run(f"python -m check_manifest --no-build-isolation {passthru}")


@task
def clean(c):
    """Clean."""
    c.run("rm -rf *.egg-info/ */*.egg-info/ dist/ build/")
