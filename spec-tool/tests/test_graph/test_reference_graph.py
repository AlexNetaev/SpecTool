"""Tests für den Referenzgraphen."""
import pytest
from spec_tool.parser.md_parser import MarkdownParser
from spec_tool.graph.reference_graph import ReferenceGraph


class TestReferenceGraph:

    def setup_method(self):
        self.parser = MarkdownParser()
        self.graph = ReferenceGraph()

    def test_build_graph(self, minimal_doc_path):
        """G-01: Graph wird aus Dokumenten aufgebaut."""
        doc = self.parser.parse_file(minimal_doc_path)
        self.graph.add_document(doc)
        self.graph.build()
        assert self.graph.node_count >= 1

    def test_broken_reference_detected(self, broken_refs_path):
        """G-02: Gebrochene Referenzen werden erkannt."""
        doc = self.parser.parse_file(broken_refs_path)
        self.graph.add_document(doc)
        self.graph.build()
        broken = self.graph.find_broken_references()
        assert len(broken) >= 1
        assert any("NONEXISTENT" in ref.target_doc for ref in broken)

    def test_valid_reference_not_broken(self, broken_refs_path):
        """G-03: Gültige Referenzen werden nicht als gebrochen markiert."""
        doc = self.parser.parse_file(broken_refs_path)
        self.graph.add_document(doc)
        self.graph.build()
        broken = self.graph.find_broken_references()
        # CHARTER §SR-04 sollte NICHT gebrochen sein (wenn CHARTER geladen ist)
        charter_broken = [r for r in broken if "CHARTER" in r.target_doc]
        assert len(charter_broken) == 0

    def test_impact_analysis(self, data_dir):
        """G-04: Impact-Analyse findet betroffene Dokumente."""
        # Alle Dateien laden
        for md_file in sorted(data_dir.rglob("*.md")):
            if "archive" in str(md_file).lower():
                continue
            doc = self.parser.parse_file(md_file)
            self.graph.add_document(doc)
        self.graph.build()

        # Impact-Analyse für CHARTER
        affected = self.graph.impact_analysis("foundation/CHARTER.md")
        assert len(affected) > 0  # CHARTER wird von vielen referenziert

    def test_statistics(self, data_dir):
        """G-05: Statistiken werden korrekt berechnet."""
        for md_file in sorted(data_dir.rglob("*.md")):
            if "archive" in str(md_file).lower():
                continue
            doc = self.parser.parse_file(md_file)
            self.graph.add_document(doc)
        self.graph.build()

        stats = self.graph.get_statistics()
        assert stats["documents"] >= 11  # 11 migrierte Dateien
        assert stats["references"] > 0
        assert stats["graph_nodes"] > 0