"""Tests für den Frontmatter-Parser."""
import pytest
from pathlib import Path
from spec_tool.parser.frontmatter import parse_frontmatter
from spec_tool.models import DocType, Layer


class TestParseFrontmatter:

    def test_valid_frontmatter(self, minimal_doc_path):
        """V-01: Gültiger Frontmatter wird korrekt geparst."""
        content = minimal_doc_path.read_text(encoding="utf-8")
        fm, rest = parse_frontmatter(content)
        assert fm is not None, "Frontmatter sollte nicht None sein"
        assert fm.doc_id == "foundation/CHARTER.md"
        assert fm.doc_type == DocType.CHARTER
        assert fm.version == "1.0.0"
        assert fm.status == "BINDEND"
        assert fm.layer == Layer.FOUNDATION

    def test_missing_frontmatter(self):
        """V-02: Datei ohne Frontmatter gibt None zurück."""
        content = "# Titel\n\nInhalt"
        fm, rest = parse_frontmatter(content)
        assert fm is None
        assert rest == content

    def test_invalid_yaml(self):
        """V-03: Ungültiges YAML gibt None zurück."""
        content = "---\ndoc_id: [invalid yaml\n---\n# Titel"
        fm, rest = parse_frontmatter(content)
        assert fm is None

    def test_frontmatter_with_builds_on(self):
        """V-04: builds_on-Liste wird korrekt geparst."""
        content = """---
doc_id: specs/QUESTOR.md
doc_type: spec
version: 1.0.0
status: BINDEND
layer: specs
builds_on:
  - foundation/CHARTER.md@1.0.0
  - foundation/CONTRACTS.md@1.2.1
---
"""
        fm, _ = parse_frontmatter(content)
        assert fm is not None
        assert len(fm.builds_on) == 2
        assert "CHARTER" in fm.builds_on[0]

    def test_unknown_doc_type_defaults_to_spec(self):
        """V-05: Unbekannter doc_type wird zu SPEC."""
        content = """---
doc_id: test.md
doc_type: unknown_type
version: 1.0.0
status: BINDEND
layer: specs
---
"""
        fm, _ = parse_frontmatter(content)
        assert fm is not None
        assert fm.doc_type == DocType.SPEC

    def test_rest_content_preserved(self, minimal_doc_path):
        """V-06: Inhalt nach Frontmatter bleibt erhalten."""
        content = minimal_doc_path.read_text(encoding="utf-8")
        fm, rest = parse_frontmatter(content)
        assert "§1 Test-Abschnitt" in rest
        assert "Inhalt hier." in rest

    # ── FIX: Neue Tests für datetime.date-Handling ──
    def test_date_parsed_as_string(self):
        """V-07: Datum wird als String geparst, nicht als datetime.date."""
        content = """---
doc_id: test.md
doc_type: spec
version: 1.0.0
status: BINDEND
layer: specs
last_modified: 2026-08-21
---
"""
        fm, _ = parse_frontmatter(content)
        assert fm is not None
        assert fm.last_modified == "2026-08-21"
        assert isinstance(fm.last_modified, str)

    def test_windows_line_endings(self):
        """V-08: Windows-Zeilenenden werden korrekt behandelt."""
        content = "---\r\ndoc_id: test.md\r\ndoc_type: spec\r\nversion: 1.0.0\r\nstatus: BINDEND\r\nlayer: specs\r\n---\r\n# Titel\r\n"
        fm, rest = parse_frontmatter(content)
        assert fm is not None
        assert fm.doc_id == "test.md"