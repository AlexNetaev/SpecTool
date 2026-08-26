"""Tests für den Markdown-Hauptparser."""
import pytest
from pathlib import Path
from spec_tool.parser.md_parser import MarkdownParser
from spec_tool.models import SectionType, DocType


class TestMarkdownParser:

    def setup_method(self):
        self.parser = MarkdownParser()

    def test_parse_minimal_doc(self, minimal_doc_path):
        """P-01: Minimale Datei wird korrekt geparst."""
        doc = self.parser.parse_file(minimal_doc_path)
        assert doc.frontmatter is not None, "Frontmatter sollte nicht None sein"
        assert doc.doc_id == "foundation/CHARTER.md"
        assert len(doc.sections) >= 1
        assert len(doc.tables) >= 1

    def test_parse_sections(self, minimal_doc_path):
        """P-02: Abschnitte werden korrekt erkannt."""
        doc = self.parser.parse_file(minimal_doc_path)
        assert len(doc.sections) >= 1
        assert doc.sections[0].title == "§1 Test-Abschnitt"
        assert doc.sections[0].section_type == SectionType.PROSE

    def test_parse_tables(self, minimal_doc_path):
        """P-03: Tabellen werden korrekt geparst."""
        doc = self.parser.parse_file(minimal_doc_path)
        assert len(doc.tables) >= 1
        table = doc.tables[0]
        # ── FIX: schema_name wird jetzt korrekt zugeordnet ──
        assert table.schema_name == "safety_rules", \
            f"Erwartet 'safety_rules', erhalten '{table.schema_name}'"
        assert table.headers == ["ID", "Regel"]
        assert len(table.rows) == 2

    def test_parse_references(self):
        """P-04: Querverweise werden extrahiert."""
        content = """---
doc_id: test.md
doc_type: spec
version: 1.0.0
status: BINDEND
layer: specs
---

## §1 Test

→ Siehe CHARTER §SR-04 für Details.
"""
        doc = self.parser.parse_content(content)
        assert len(doc.references) >= 1
        ref = doc.references[0]
        assert "CHARTER" in ref.target_doc
        assert ref.target_section == "SR-04"

    def test_parse_errors_collected(self):
        """P-05: Parse-Fehler werden gesammelt."""
        content = "# Kein Frontmatter"
        doc = self.parser.parse_content(content)
        assert len(doc.parse_errors) >= 1

    def test_get_section(self, minimal_doc_path):
        """P-06: get_section() findet Abschnitt nach ID."""
        doc = self.parser.parse_file(minimal_doc_path)
        section = doc.get_section("1")
        assert section is not None
        assert "Test-Abschnitt" in section.title

    def test_get_sections_by_type(self, minimal_doc_path):
        """P-07: get_sections_by_type() filtert korrekt."""
        doc = self.parser.parse_file(minimal_doc_path)
        prose = doc.get_sections_by_type(SectionType.PROSE)
        assert len(prose) >= 1

    def test_doc_properties(self, minimal_doc_path):
        """P-08: Doc-Properties funktionieren."""
        doc = self.parser.parse_file(minimal_doc_path)
        # ── FIX: version wird jetzt korrekt aus Frontmatter gelesen ──
        assert doc.version == "1.0.0", \
            f"Erwartet '1.0.0', erhalten '{doc.version}'"
        assert doc.layer is not None
        assert doc.section_count >= 1

    # ── FIX: Neue Tests für @ref-Marker ──
    def test_parse_ref_markers(self):
        """P-09: @ref-Marker werden als Referenzen behandelt."""
        content = """---
doc_id: test.md
doc_type: spec
version: 1.0.0
status: BINDEND
layer: specs
---

## §1 Test

<!-- @ref target="CHARTER §SR-04" type="security-rule" -->
→ Siehe CHARTER §SR-04 für Details.

<!-- @ref target="NONEXISTENT §99.99" type="spec" -->
→ Siehe NONEXISTENT §99.99 für Details.
"""
        doc = self.parser.parse_content(content)
        assert len(doc.references) >= 2

        # Prüfe dass beide Referenzen gefunden wurden
        targets = [r.target_doc for r in doc.references]
        assert any("CHARTER" in t for t in targets), "CHARTER-Referenz nicht gefunden"
        assert any("NONEXISTENT" in t for t in targets), "NONEXISTENT-Referenz nicht gefunden"