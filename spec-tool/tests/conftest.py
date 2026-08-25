"""Gemeinsame Fixtures für alle Tests."""
import pytest
from pathlib import Path

FIXTURES_DIR = Path(__file__).parent / "fixtures"
DATA_DIR = Path(__file__).parent.parent / "data"


@pytest.fixture
def fixtures_dir():
    """Pfad zum fixtures/-Verzeichnis."""
    return FIXTURES_DIR


@pytest.fixture
def data_dir():
    """Pfad zum data/-Verzeichnis (migrierte MYRMEX-Dateien)."""
    return DATA_DIR


@pytest.fixture
def minimal_doc_path():
    """Pfad zur minimalen Testdatei."""
    return FIXTURES_DIR / "minimal_doc.md"


@pytest.fixture
def broken_refs_path():
    """Pfad zur Datei mit gebrochenen Referenzen."""
    return FIXTURES_DIR / "broken_refs.md"


@pytest.fixture
def all_spec_files(data_dir):
    """Alle migrierten Spezifikationsdateien."""
    files = []
    for pattern in ["**/*.md"]:
        files.extend(data_dir.glob(pattern))
    # Archivierte Dateien ausschließen
    files = [f for f in files if "archive" not in str(f).lower()]
    return sorted(files)


@pytest.fixture
def charter_path(data_dir):
    """Pfad zur CHARTER.md."""
    return data_dir / "foundation" / "CHARTER.md"


@pytest.fixture
def contracts_path(data_dir):
    """Pfad zur CONTRACTS.md."""
    return data_dir / "foundation" / "CONTRACTS.md"