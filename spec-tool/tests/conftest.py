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
    if data_dir.exists():
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


# ── FIX: Fixture für E2E-Tests, die Dateien im data/-Verzeichnis erstellt ──
@pytest.fixture(autouse=False)
def ensure_data_files(data_dir):
    """
    Erstellt die data/-Verzeichnisstruktur mit den migrierten Dateien,
    falls sie nicht existieren.
    """
    # Verzeichnisse erstellen
    (data_dir / "foundation").mkdir(parents=True, exist_ok=True)
    (data_dir / "specs").mkdir(parents=True, exist_ok=True)
    (data_dir / "ops").mkdir(parents=True, exist_ok=True)

    # Prüfe ob Dateien existieren
    required_files = [
        data_dir / "foundation" / "CHARTER.md",
        data_dir / "foundation" / "CONTRACTS.md",
        data_dir / "foundation" / "SPEC_FORMAT.md",
        data_dir / "specs" / "GREMIUM.md",
        data_dir / "specs" / "GREMIUM_STRATEGY.md",
        data_dir / "specs" / "QUESTOR.md",
        data_dir / "specs" / "HAL.md",
        data_dir / "specs" / "CAROUSEL_TWIN.md",
        data_dir / "ops" / "VALIDATION.md",
        data_dir / "ops" / "VALIDATION_ATLAS.md",
        data_dir / "ops" / "ROADMAP.md",
    ]

    missing = [f for f in required_files if not f.exists()]
    if missing:
        pytest.skip(
            f"Fehlende Dateien im data/-Verzeichnis: "
            f"{', '.join(str(f.name) for f in missing)}. "
            f"Bitte migrierte Dateien in data/ kopieren."
        )

    return required_files