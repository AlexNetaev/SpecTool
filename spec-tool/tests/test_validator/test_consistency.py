"""Tests für den Konsistenz-Validator."""
import pytest
from spec_tool.parser.md_parser import MarkdownParser
from spec_tool.validator.consistency import ConsistencyValidator


class TestConsistencyValidator:

    def setup_method(self):
        self.parser = MarkdownParser()
        self.validator = ConsistencyValidator()

    def test_valid_document_passes(self, minimal_doc_path):
        """C-01: Gültiges Dokument besteht die Validierung."""
        doc = self.parser.parse_file(minimal_doc_path)
        report = self.validator.validate([doc])
        # Minimal-Dokument sollte keine ERRORs haben
        assert len(report.errors) == 0

    def test_missing_frontmatter_detected(self):
        """C-02: Fehlender Frontmatter wird erkannt."""
        content = "# Kein Frontmatter"
        doc = self.parser.parse_content(content)
        report = self.validator.validate([doc])
        assert any(r.rule_id == "V-01" for r in report.results)

    def test_broken_reference_warning(self, broken_refs_path):
        """C-03: Gebrochene Referenzen erzeugen Warnungen."""
        doc = self.parser.parse_file(broken_refs_path)
        report = self.validator.validate([doc])
        assert any(r.rule_id == "V-06" for r in report.results)

    def test_all_myrmex_files_valid(self, data_dir):
        """C-04: Alle migrierten MYRMEX-Dateien sind valide."""
        docs = []
        for md_file in sorted(data_dir.rglob("*.md")):
            if "archive" in str(md_file).lower():
                continue
            doc = self.parser.parse_file(md_file)
            docs.append(doc)

        report = self.validator.validate(docs)
        # Keine ERRORs erlaubt (Warnungen sind OK)
        for error in report.errors:
            print(f"ERROR: {error.rule_id} - {error.message} ({error.file_path})")
        assert len(report.errors) == 0, f"{len(report.errors)} Fehler gefunden"

    def test_report_summary(self, minimal_doc_path):
        """C-05: Report-Zusammenfassung ist korrekt."""
        doc = self.parser.parse_file(minimal_doc_path)
        report = self.validator.validate([doc])
        summary = report.summary()
        assert "Dokumente geprüft:" in summary
        assert "GÜLTIG" in summary or "UNGÜLTIG" in summary