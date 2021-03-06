"""Pytest configuration."""
import os
import shutil
import tempfile
from pathlib import Path

import pytest

# Use a fixed temporary root to help debugging locally; otherwise, a temporary root will be used.
# On macOS, use /private/tmp as the root instead of /tmp, otherwise lots of tests will fail.
NITPICK_TEST_DIR = os.environ.get("NITPICK_TEST_DIR")
TEMP_ROOT_PATH = Path(NITPICK_TEST_DIR or tempfile.mkdtemp()).expanduser().absolute()


@pytest.fixture("session", autouse=True)
def delete_project_temp_root():
    """Delete the temporary root before or after running the tests, depending on the env variable."""
    if NITPICK_TEST_DIR:
        # If the environment variable is configured, delete its contents before the tests.
        if TEMP_ROOT_PATH.exists():
            shutil.rmtree(str(TEMP_ROOT_PATH))
        TEMP_ROOT_PATH.mkdir()

    yield

    if not NITPICK_TEST_DIR:
        # If the environment variable is not configured, then a random temp dir will be used;
        # its contents should be deleted after the tests.
        shutil.rmtree(str(TEMP_ROOT_PATH))
