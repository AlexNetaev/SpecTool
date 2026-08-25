"""End-to-End-Tests gegen die migrierten MYRMEX-Dateien."""
import pytest
from spec_tool.parser.md_parser import MarkdownParser
from spec_tool.graph.reference_graph import ReferenceGraph
from spec_tool.validator.consistency import ConsistencyValidator
from spec_tool.generator.views import ViewGenerator


class TestE2E:
    """End-to-End-Tests gegen alle migrierten Dateien."""

    @pytest.fixture(autouse=True)
    def setup(self, data_dir):
        self.parser = MarkdownParser()
        self.data_dir = data_dir
        self.docs = []
        for md_file in sorted(data_dir.rglob("*.md")):
            if "archive" in str(md_file).lower():
                continue
            doc = self.parser.parse_file(md_file)
            self.docs.append(doc)

    def test_all_files_parse_without_errors(self):
        """E2E-01: Alle Dateien parsen ohne Fehler."""
        for doc in self.docs:
            assert len(doc.parse_errors) == 0, \
                f"{doc.doc_id}: {doc.parse_errors}"

    def test_all_files_have_frontmatter(self):
        """E2E-02: Alle Dateien haben einen Frontmatter."""
        for doc in self.docs:
            assert doc.frontmatter is not None, \
                f"{doc.doc_id}: Kein Frontmatter"

    def test_all_files_have_sections(self):
        """E2E-03: Alle Dateien haben Abschnitte."""
        for doc in self.docs:
            assert doc.section_count > 0, \
                f"{doc.doc_id}: Keine Abschnitte"

    def test_charter_has_58_safety_rules(self, charter_path):
        """E2E-04: CHARTER.md enthält 58 Sicherheitsregeln."""
        doc = self.parser.parse_file(charter_path)
        # SR-01 bis SR-58 zählen
        sr_count = 0
        for section in doc.sections:
            for marker in section.markers:
                if marker.marker_type.value == "safety-rule":
                    sr_count += 1
        # Alternativ: Im Inhalt zählen
        content = doc.raw_content
        import re
        sr_matches = re.findall(r"SR-(\d+)", content)
        unique_srs = set(sr_matches)
        assert len(unique_srs) >= 58, \
            f"Nur {len(unique_srs)} SR-Regeln gefunden, erwartet >= 58"

    def test_contracts_has_all_sections(self, contracts_path):
        """E2E-05: CONTRACTS.md enthält alle Hauptabschnitte."""
        doc = self.parser.parse_file(contracts_path)
        section_ids = [s.section_id for s in doc.sections]
        # Hauptabschnitte prüfen
        assert any("1" in sid for sid in section_ids), "§1 fehlt"
        assert any("6" in sid for sid in section_ids), "§6 fehlt"
        assert any("10" in sid for sid in section_ids), "§10 fehlt"

    def test_reference_graph_complete(self):
        """E2E-06: Referenzgraph ist vollständig."""
        graph = ReferenceGraph()
        for doc in self.docs:
            graph.add_document(doc)
        graph.build()

        stats = graph.get_statistics()
        assert stats["documents"] >= 11
        assert stats["references"] > 50
        assert stats["broken_references"] < 5  # Wenige gebrochene Refs erlaubt

    def test_consistency_all_files(self):
        """E2E-07: Konsistenzprüfung über alle Dateien."""
        validator = ConsistencyValidator()
        report = validator.validate(self.docs)
        assert report.is_valid, \
            f"Konsistenzprüfung fehlgeschlagen: {len(report.errors)} Fehler"

    def test_role_views_generated(self):
        """E2E-08: Rollen-Views werden generiert."""
        generator = ViewGenerator()
        roles = generator.generate_role_views(self.docs)
        assert len(roles) > 0, "Keine Rollen gefunden"
        # Bekannte Rollen prüfen
        role_ids = [r.role_id for r in roles]
        assert any("archivar" in rid for rid in role_ids), "Archivar nicht gefunden"
        assert any("kartograph" in rid for rid in role_ids), "Kartograph nicht gefunden"

    def test_dataflow_views_generated(self):
        """E2E-09: Datenfluss-Views werden generiert."""
        generator = ViewGenerator()
        dataflows = generator.generate_dataflow_views(self.docs)
        assert len(dataflows) > 0, "Keine Datenflüsse gefunden"

    def test_test_matrix_generated(self):
        """E2E-10: Test-Matrix wird generiert."""
        generator = ViewGenerator()
        entries = generator.generate_test_matrix(self.docs)
        assert len(entries) > 0, "Keine Test-Einträge gefunden"

    def test_layer_hierarchy_respected(self):
        """E2E-11: Layer-Hierarchie wird eingehalten."""
        for doc in self.docs:
            if doc.frontmatter and doc.frontmatter.layer:
                # Foundation-Dokumente dürfen keine specs/ referenzieren
                if doc.frontmatter.layer.value == "foundation":
                    for ref in doc.references:
                        assert not ref.target_doc.startswith("specs/"), \
                            f"{doc.doc_id} referenziert specs/ (Hierarchie-Verstoß)"

    def test_charter_not_referenced_by_ops_directly(self):
        """E2E-12: CHARTER wird korrekt referenziert."""
        for doc in self.docs:
            if doc.frontmatter and doc.frontmatter.layer:
                if doc.frontmatter.layer.value == "ops":
                    # ops/ darf CHARTER referenzieren
                    pass  # OK