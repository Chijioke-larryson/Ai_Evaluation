from pathlib import Path

import pytest

from src.database import init_db


@pytest.fixture
def db_path(tmp_path: Path) -> Path:
    path = tmp_path / "test.sqlite"
    init_db(path)
    return path

