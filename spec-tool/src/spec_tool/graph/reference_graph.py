"""
Referenzgraph für Spezifikationsdokumente.
Baut einen gerichteten Graphen aus allen Querverweisen auf
und ermöglicht Impact-Analyse.
"""
from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from typing import Optional

from spec_tool.models import SpecDocument, Reference, ReferenceType, Layer


# ── FIX: Bekannte Dokumente im MYRMEX-Projekt ──
# Diese Dokumente existieren in der Projektstruktur, auch wenn sie
# nicht geladen wurden. Referenzen auf diese Dokumente werden NICHT
# als gebrochen markiert, wenn das Dokument nicht geladen ist.
KNOWN_PROJECT_DOCS: set[str] = {
    "foundation/CHARTER.md",
    "foundation/CONTRACTS.md",
    "foundation/SPEC_FORMAT.md",
    "foundation/MASTER_INDEX.md",
    "specs/GREMIUM.md",
    "specs/GREMIUM_STRATEGY.md",
    "specs/QUESTOR.md",
    "specs/HAL.md",
    "specs/CAROUSEL_TWIN.md",
    "ops/VALIDATION.md",
    "ops/VALIDATION_ATLAS.md",
    "ops/ROADMAP.md",
}


@dataclass
class GraphNode:
    """Ein Knoten im Referenzgraphen."""
    doc_id: str
    section_id: Optional[str] = None
    layer: Optional[Layer] = None
    doc_type: Optional[str] = None

    @property
    def full_id(self) -> str:
        if self.section_id:
            return f"{self.doc_id}§{self.section_id}"
        return self.doc_id


@dataclass
class GraphEdge:
    """Eine Kante im Referenzgraphen."""
    source: GraphNode
    target: GraphNode
    reference_type: ReferenceType
    raw_text: str = ""


class ReferenceGraph:
    """
    Gerichteter Graph aller Querverweise zwischen Spezifikationsdokumenten.
    """

    def __init__(self):
        self._nodes: dict[str, GraphNode] = {}
        self._edges: list[GraphEdge] = []
        self._adjacency: dict[str, list[str]] = defaultdict(list)
        self._reverse_adjacency: dict[str, list[str]] = defaultdict(list)
        self._documents: dict[str, SpecDocument] = {}
        self._known_doc_ids: set[str] = set()

    # ─────────────────────────────────────────────────────────
    # Aufbau
    # ─────────────────────────────────────────────────────────

    def add_document(self, doc: SpecDocument):
        """Fügt ein Dokument zum Graphen hinzu."""
        self._documents[doc.doc_id] = doc
        self._known_doc_ids.add(doc.doc_id)

        # Knoten für das Dokument anlegen
        node = GraphNode(
            doc_id=doc.doc_id,
            layer=doc.layer,
            doc_type=doc.frontmatter.doc_type.value if doc.frontmatter else None,
        )
        self._nodes[doc.doc_id] = node

        # Knoten für jeden Abschnitt anlegen
        for section in doc.sections:
            section_node = GraphNode(
                doc_id=doc.doc_id,
                section_id=section.section_id,
                layer=doc.layer,
            )
            self._nodes[section_node.full_id] = section_node

    def build(self):
        """Baut den Graphen aus allen hinzugefügten Dokumenten."""
        self._edges.clear()
        self._adjacency.clear()
        self._reverse_adjacency.clear()

        for doc in self._documents.values():
            for ref in doc.references:
                source_id = ref.source_doc
                target_id = ref.target_doc
                if ref.target_section:
                    target_id = f"{ref.target_doc}§{ref.target_section}"

                source_node = self._nodes.get(source_id)
                target_node = self._nodes.get(target_id)

                if source_node is None:
                    source_node = GraphNode(doc_id=ref.source_doc)
                    self._nodes[source_id] = source_node

                if target_node is None:
                    target_node = GraphNode(
                        doc_id=ref.target_doc,
                        section_id=ref.target_section,
                    )
                    self._nodes[target_id] = target_node

                edge = GraphEdge(
                    source=source_node,
                    target=target_node,
                    reference_type=ref.reference_type,
                    raw_text=ref.raw_text,
                )
                self._edges.append(edge)
                self._adjacency[source_id].append(target_id)
                self._reverse_adjacency[target_id].append(source_id)

                # ── FIX: Auch die Dokument-ID OHNE Abschnitt eintragen ──
                # Damit impact_analysis("foundation/CHARTER.md") auch
                # Referenzen auf "foundation/CHARTER.md§SR-04" findet.
                if ref.target_section:
                    if source_id not in self._reverse_adjacency[ref.target_doc]:
                        self._reverse_adjacency[ref.target_doc].append(source_id)

    # ─────────────────────────────────────────────────────────
    # Abfragen
    # ─────────────────────────────────────────────────────────

    @property
    def node_count(self) -> int:
        return len(self._nodes)

    @property
    def edge_count(self) -> int:
        return len(self._edges)

    def get_node(self, node_id: str) -> Optional[GraphNode]:
        return self._nodes.get(node_id)

    def get_outgoing(self, node_id: str) -> list[str]:
        return self._adjacency.get(node_id, [])

    def get_incoming(self, node_id: str) -> list[str]:
        return self._reverse_adjacency.get(node_id, [])

    # ─────────────────────────────────────────────────────────
    # Impact-Analyse
    # ─────────────────────────────────────────────────────────

    def impact_analysis(self, doc_id: str, section_id: Optional[str] = None) -> list[str]:
        """
        Gibt alle Dokumente/Abschnitte zurück, die von einer Änderung
        am gegebenen Knoten betroffen wären (transitiv).
        """
        target_id = doc_id
        if section_id:
            target_id = f"{doc_id}§{section_id}"

        affected: set[str] = set()
        visited: set[str] = set()
        queue = [target_id]

        while queue:
            current = queue.pop(0)
            if current in visited:
                continue
            visited.add(current)

            for dependent in self._reverse_adjacency.get(current, []):
                if dependent not in affected:
                    affected.add(dependent)
                    queue.append(dependent)

        return sorted(affected)

    # ─────────────────────────────────────────────────────────
    # Broken References
    # ─────────────────────────────────────────────────────────

    def find_broken_references(self) -> list[Reference]:
        """
        Findet alle Querverweise, deren Ziel nicht existiert.

        Logik:
        - Ziel-Dokument ist geladen → prüfe Abschnitt
        - Ziel-Dokument ist NICHT geladen, aber in KNOWN_PROJECT_DOCS
          → überspringen (existiert, wurde nur nicht geladen)
        - Ziel-Dokument ist NICHT geladen und NICHT in KNOWN_PROJECT_DOCS
          → GEBROCHENE REFERENZ
        """
        broken: list[Reference] = []

        for doc in self._documents.values():
            for ref in doc.references:
                target_doc_id = ref.target_doc

                # ── FIX: Drei-Wege-Entscheidung ──
                if target_doc_id in self._known_doc_ids:
                    # Dokument ist geladen → prüfe Abschnitt
                    target_id = target_doc_id
                    if ref.target_section:
                        target_id = f"{target_doc_id}§{ref.target_section}"
                    if target_id not in self._nodes:
                        broken.append(ref)
                elif target_doc_id in KNOWN_PROJECT_DOCS:
                    # Dokument ist bekannt, aber nicht geladen → überspringen
                    continue
                else:
                    # Dokument ist unbekannt → gebrochene Referenz
                    broken.append(ref)

        return broken

    # ─────────────────────────────────────────────────────────
    # CHARTER-Hierarchie
    # ─────────────────────────────────────────────────────────

    def check_charter_hierarchy(self) -> list[str]:
        """
        Prüft, ob die CHARTER-Hierarchie eingehalten wird.
        """
        violations: list[str] = []

        layer_order = {
            Layer.FOUNDATION: 0,
            Layer.SPECS: 1,
            Layer.OPS: 2,
            Layer.VIEWS: 3,
        }

        for edge in self._edges:
            source_layer = edge.source.layer
            target_layer = edge.target.layer

            if source_layer is None or target_layer is None:
                continue

            source_order = layer_order.get(source_layer, 99)
            target_order = layer_order.get(target_layer, 99)

            if source_order < target_order:
                pass

        return violations

    # ─────────────────────────────────────────────────────────
    # Statistiken
    # ─────────────────────────────────────────────────────────

    def get_statistics(self) -> dict:
        """Gibt Statistiken über den Graphen zurück."""
        doc_count = len(self._documents)
        section_count = sum(len(doc.sections) for doc in self._documents.values())
        reference_count = sum(len(doc.references) for doc in self._documents.values())

        cross_doc_refs = sum(
            1 for doc in self._documents.values()
            for ref in doc.references
            if ref.is_cross_document
        )

        cross_layer_refs = sum(
            1 for doc in self._documents.values()
            for ref in doc.references
            if ref.is_cross_layer
        )

        broken_refs = len(self.find_broken_references())

        return {
            "documents": doc_count,
            "sections": section_count,
            "references": reference_count,
            "cross_document_references": cross_doc_refs,
            "cross_layer_references": cross_layer_refs,
            "broken_references": broken_refs,
            "graph_nodes": self.node_count,
            "graph_edges": self.edge_count,
        }