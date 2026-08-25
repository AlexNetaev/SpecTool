"""Tests für den Konsistenz-Validator."""
import pytest
from pathlib import Path
from spec_tool.parser.md_parser import MarkdownParser
from spec_tool.validator.consistency import ConsistencyValidator, ValidationReport


class TestConsistencyValidator:

    def setup_method(self):
        self.parser = MarkdownParser()
        self.validator = ConsistencyValidator()

    def test_valid_document(self):
        content = """---
doc_id: foundation/CHARTER.md
doc_type: charter
version: 1.0.0
status: BINDEND
layer: foundation
builds_on: []
---

## §1 Test

Inhalt.
"""
        doc = self.parser.parse_content(content, Path("foundation/CHARTER.md"))
        report = self.validator.validate([doc])
        assert report.is_valid

    def test_missing_frontmatter(self):
        content = "# Kein Frontmatter"
        doc = self.parser.parse_content(content, Path("test.md"))
        report = self.validator.validate([doc])
        assert not report.is_valid
        assert any(r.rule_id == "V-01" for r in report.errors)

    def test_missing_doc_id(self):
        content = """---
doc_type: spec
version: 1.0.0
status: BINDEND
layer: specs
---
"""
        doc = self.parser.parse_content(content, Path("test.md"))
        report = self.validator.validate([doc])
        assert any(r.rule_id == "V-02" for r in report.results)

    def test_broken_reference(self):
        content = """---
doc_id: specs/QUESTOR.md
doc_type: spec
version: 1.0.0
status: BINDEND
layer: specs
---

## §1 Test

→ Siehe NONEXISTENT §99.99 für Details.
"""
        doc = self.parser.parse_content(content, Path("specs/QUESTOR.md"))
        report = self.validator.validate([doc])
        assert any(r.rule_id == "V-06" for r in report.results)

    def test_version_consistency(self):
        charter_content = """---
doc_id: foundation/CHARTER.md
doc_type: charter
version: 1.0.0
status: BINDEND
layer: foundation
---
"""
        spec_content = """---
doc_id: specs/QUESTOR.md
doc_type: spec
version: 1.0.0
status: BINDEND
layer: specs
builds_on:
  - foundation/CHARTER.md@2.0.0
---
"""
        charter_doc = self.parser.parse_content(charter_content, Path("foundation/CHARTER.md"))
        spec_doc = self.parser.parse_content(spec_content, Path("specs/QUESTOR.md"))
        report = self.validator.validate([charter_doc, spec_doc])
        assert any(r.rule_id == "V-11" for r in report.results)

    def test_report_summary(self):
        content = """---
doc_id: test.md
doc_type: spec
version: 1.0.0
status: BINDEND
layer: specs
---
"""
        doc = self.parser.parse_content(content, Path("test.md"))
        report = self.validator.validate([doc])
        summary = report.summary()
        assert "Dokumente geprüft: 1" in summary
        assert "GÜLTIG" in summary