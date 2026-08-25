"""Tests für den Markdown-Hauptparser."""
import pytest
from pathlib import Path
from spec_tool.parser.md_parser import MarkdownParser
from spec_tool.models import SectionType, MarkerType


class TestMarkdownParser:

    def setup_method(self):
        self.parser = MarkdownParser()

    def test_parse_simple_document(self):
        content = """---
doc_id: test.md
doc_type: spec
version: 1.0.0
status: BINDEND
layer: specs
---

# Titel

Inhalt hier.
"""
        doc = self.parser.parse_content(content, Path("test.md"))
        assert doc.frontmatter is not None
        assert doc.doc_id == "test.md"
        assert len(doc.sections) >= 1

    def test_parse_sections(self):
        content = """---
doc_id: test.md
doc_type: spec
version: 1.0.0
status: BINDEND
layer: specs
---

## §1 Erster Abschnitt

Inhalt.

## §2 Zweiter Abschnitt

Mehr Inhalt.
"""
        doc = self.parser.parse_content(content, Path("test.md"))
        assert len(doc.sections) >= 2
        assert doc.sections[0].title == "§1 Erster Abschnitt"
        assert doc.sections[1].title == "§2 Zweiter Abschnitt"

    def test_parse_section_markers(self):
        content = """---
doc_id: test.md
doc_type: spec
version: 1.0.0
status: BINDEND
layer: specs
---

<!-- @section id="3.2" title="Kartograph" type="role-definition" -->
<!-- @role id="kartograph" layer="4" llm="false" -->
## §3.2 Kartograph

Inhalt.
"""
        doc = self.parser.parse_content(content, Path("test.md"))
        assert len(doc.sections) >= 1
        section = doc.sections[0]
        assert section.section_type == SectionType.ROLE_DEFINITION
        assert section.role_id == "kartograph"
        assert section.role_layer == 4
        assert section.role_llm is False

    def test_parse_tables(self):
        content = """---
doc_id: test.md
doc_type: spec
version: 1.0.0
status: BINDEND
layer: specs
---

## §1 Test

<!-- @table schema="role_permissions" role="test" -->
| Erlaubt | Verboten |
|---------|----------|
| Lesen | Schreiben |
"""
        doc = self.parser.parse_content(content, Path("test.md"))
        assert len(doc.tables) >= 1
        table = doc.tables[0]
        assert table.schema_name == "role_permissions"
        assert table.headers == ["Erlaubt", "Verboten"]
        assert len(table.rows) == 1
        assert table.rows[0] == ["Lesen", "Schreiben"]

    def test_parse_references(self):
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
        doc = self.parser.parse_content(content, Path("test.md"))
        assert len(doc.references) >= 1
        ref = doc.references[0]
        assert ref.target_doc == "foundation/CHARTER.md"
        assert ref.target_section == "SR-04"

    def test_parse_errors_collected(self):
        content = "# Kein Frontmatter"
        doc = self.parser.parse_content(content, Path("test.md"))
        assert len(doc.parse_errors) >= 1
        assert "Kein gültiger YAML-Frontmatter" in doc.parse_errors[0]

    def test_get_section(self):
        content = """---
doc_id: test.md
doc_type: spec
version: 1.0.0
status: BINDEND
layer: specs
---

## §1 Erster

Inhalt.

## §2 Zweiter

Mehr Inhalt.
"""
        doc = self.parser.parse_content(content, Path("test.md"))
        section = doc.get_section("1")
        assert section is not None
        assert section.title == "§1 Erster"

    def test_get_sections_by_type(self):
        content = """---
doc_id: test.md
doc_type: spec
version: 1.0.0
status: BINDEND
layer: specs
---

<!-- @section id="1" title="Rolle" type="role-definition" -->
## §1 Rolle

<!-- @section id="2" title="Text" type="prose" -->
## §2 Text
"""
        doc = self.parser.parse_content(content, Path("test.md"))
        roles = doc.get_sections_by_type(SectionType.ROLE_DEFINITION)
        assert len(roles) == 1
        assert roles[0].title == "§1 Rolle"