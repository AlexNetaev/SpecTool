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
        assert fm is not None
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