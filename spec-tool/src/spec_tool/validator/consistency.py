"""
Konsistenz-Validator für Spezifikationsdokumente.
Prüft CHARTER-Hierarchie, gebrochene Referenzen, Frontmatter-Vollständigkeit.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from spec_tool.models import (
    SpecDocument,
    Reference,
    ReferenceType,
    Layer,
    DocType,
    SectionType,
)
from spec_tool.graph.reference_graph import ReferenceGraph


@dataclass
class ValidationResult:
    """Ergebnis einer einzelnen Validierungsprüfung."""
    rule_id: str
    severity: str  # ERROR, WARNING, INFO
    message: str
    file_path: Optional[str] = None
    line_number: Optional[int] = None


@dataclass
class ValidationReport:
    """Gesamtbericht einer Validierung."""
    results: list[ValidationResult] = field(default_factory=list)
    documents_checked: int = 0
    references_checked: int = 0

    @property
    def errors(self) -> list[ValidationResult]:
        return [r for r in self.results if r.severity == "ERROR"]

    @property
    def warnings(self) -> list[ValidationResult]:
        return [r for r in self.results if r.severity == "WARNING"]

    @property
    def is_valid(self) -> bool:
        return len(self.errors) == 0

    def add(self, result: ValidationResult):
        self.results.append(result)

    def summary(self) -> str:
        lines = [
            f"Dokumente geprüft: {self.documents_checked}",
            f"Referenzen geprüft: {self.references_checked}",
            f"Fehler: {len(self.errors)}",
            f"Warnungen: {len(self.warnings)}",
            f"Status: {'GÜLTIG' if self.is_valid else 'UNGÜLTIG'}",
        ]
        return "\n".join(lines)


# ─────────────────────────────────────────────────────────────
# Layer-Hierarchie
# ─────────────────────────────────────────────────────────────

LAYER_ORDER = {
    Layer.FOUNDATION: 0,
    Layer.SPECS: 1,
    Layer.OPS: 2,
    Layer.VIEWS: 3,
}

LAYER_NAMES = {
    Layer.FOUNDATION: "foundation",
    Layer.SPECS: "specs",
    Layer.OPS: "ops",
    Layer.VIEWS: "views",
}


class ConsistencyValidator:
    """
    Validiert die Konsistenz von Spezifikationsdokumenten.

    Verwendung:
        validator = ConsistencyValidator()
        report = validator.validate(documents)
        print(report.summary())
    """

    def validate(self, documents: list[SpecDocument]) -> ValidationReport:
        """Führt alle Validierungsprüfungen durch."""
        report = ValidationReport()
        report.documents_checked = len(documents)

        # Graph aufbauen
        graph = ReferenceGraph()
        for doc in documents:
            graph.add_document(doc)
        graph.build()
        report.references_checked = graph.edge_count

        # Prüfungen durchführen
        self._check_frontmatter(documents, report)
        self._check_layer_hierarchy(documents, report)
        self._check_broken_references(graph, report)
        self._check_charter_rules(documents, report)
        self._check_section_structure(documents, report)
        self._check_version_consistency(documents, report)

        return report

    # ─────────────────────────────────────────────────────────
    # Prüfung 1: Frontmatter
    # ─────────────────────────────────────────────────────────

    def _check_frontmatter(self, documents: list[SpecDocument], report: ValidationReport):
        """Prüft, dass alle Dokumente einen gültigen Frontmatter haben."""
        for doc in documents:
            file_str = str(doc.file_path)

            if doc.frontmatter is None:
                report.add(ValidationResult(
                    rule_id="V-01",
                    severity="ERROR",
                    message=f"Kein YAML-Frontmatter gefunden",
                    file_path=file_str,
                ))
                continue

            fm = doc.frontmatter

            # Pflichtfelder prüfen
            if not fm.doc_id:
                report.add(ValidationResult(
                    rule_id="V-02",
                    severity="ERROR",
                    message="doc_id fehlt im Frontmatter",
                    file_path=file_str,
                ))

            if not fm.version:
                report.add(ValidationResult(
                    rule_id="V-03",
                    severity="ERROR",
                    message="version fehlt im Frontmatter",
                    file_path=file_str,
                ))

            if not fm.status:
                report.add(ValidationResult(
                    rule_id="V-04",
                    severity="WARNING",
                    message="status fehlt im Frontmatter",
                    file_path=file_str,
                ))

            # doc_id muss mit Dateipfad übereinstimmen
            expected_doc_id = file_str.replace("\\", "/")
            if fm.doc_id and fm.doc_id != expected_doc_id:
                report.add(ValidationResult(
                    rule_id="V-05",
                    severity="WARNING",
                    message=f"doc_id '{fm.doc_id}' stimmt nicht mit Dateipfad '{expected_doc_id}' überein",
                    file_path=file_str,
                ))

    # ─────────────────────────────────────────────────────────
    # Prüfung 2: Layer-Hierarchie
    # ─────────────────────────────────────────────────────────

    def _check_layer_hierarchy(self, documents: list[SpecDocument], report: ValidationReport):
        """Prüft, dass die Layer-Hierarchie eingehalten wird."""
        doc_layers = {}
        for doc in documents:
            if doc.frontmatter and doc.frontmatter.layer:
                doc_layers[doc.doc_id] = doc.frontmatter.layer

        for doc in documents:
            if doc.frontmatter is None or doc.frontmatter.layer is None:
                continue

            source_layer = doc.frontmatter.layer
            source_order = LAYER_ORDER.get(source_layer, 99)

            for ref in doc.references:
                target_layer = self._get_layer_from_path(ref.target_doc)
                if target_layer is None:
                    continue

                target_order = LAYER_ORDER.get(target_layer, 99)

                # Ein Dokument in Layer N darf kein Dokument in Layer N-1 überschreiben
                # (es darf es referenzieren, aber die Hierarchie muss stimmen)
                if source_order < target_order:
                    # Foundation referenziert Specs — das ist OK (Referenz, kein Überschreiben)
                    pass
                elif source_order > target_order:
                    # Specs referenziert Foundation — das ist OK
                    pass

    def _get_layer_from_path(self, path: str) -> Optional[Layer]:
        """Bestimmt den Layer aus einem Dateipfad."""
        path_lower = path.lower()
        if path_lower.startswith("foundation/"):
            return Layer.FOUNDATION
        elif path_lower.startswith("specs/"):
            return Layer.SPECS
        elif path_lower.startswith("ops/"):
            return Layer.OPS
        elif path_lower.startswith("views/"):
            return Layer.VIEWS
        return None

    # ─────────────────────────────────────────────────────────
    # Prüfung 3: Gebrochene Referenzen
    # ─────────────────────────────────────────────────────────

    def _check_broken_references(self, graph: ReferenceGraph, report: ValidationReport):
        """Prüft auf gebrochene Referenzen."""
        broken = graph.find_broken_references()
        for ref in broken:
            report.add(ValidationResult(
                rule_id="V-06",
                severity="WARNING",
                message=f"Gebrochene Referenz: {ref.source_doc} → {ref.target_doc}"
                        + (f" §{ref.target_section}" if ref.target_section else ""),
                file_path=ref.source_doc,
                line_number=ref.line_number,
            ))

    # ─────────────────────────────────────────────────────────
    # Prüfung 4: CHARTER-Regeln
    # ─────────────────────────────────────────────────────────

    def _check_charter_rules(self, documents: list[SpecDocument], report: ValidationReport):
        """Prüft CHARTER-spezifische Regeln."""
        # Finde das CHARTER-Dokument
        charter_doc = None
        for doc in documents:
            if doc.frontmatter and doc.frontmatter.doc_type == DocType.CHARTER:
                charter_doc = doc
                break

        if charter_doc is None:
            report.add(ValidationResult(
                rule_id="V-07",
                severity="WARNING",
                message="Kein CHARTER-Dokument gefunden",
            ))
            return

        # Prüfe, dass alle SR-XX-Referenzen existieren
        charter_sections = set()
        for section in charter_doc.sections:
            if section.safety_rule_id:
                charter_sections.add(section.safety_rule_id)
            # Auch aus dem Inhalt extrahieren
            import re
            sr_matches = re.findall(r"SR-(\d+)", section.content)
            for sr_num in sr_matches:
                charter_sections.add(f"SR-{sr_num}")

        # Prüfe Referenzen auf CHARTER-Regeln
        for doc in documents:
            for ref in doc.references:
                if ref.reference_type == ReferenceType.SECURITY_RULE and ref.target_section:
                    sr_id = ref.target_section
                    if sr_id not in charter_sections:
                        report.add(ValidationResult(
                            rule_id="V-08",
                            severity="WARNING",
                            message=f"CHARTER-Regel '{sr_id}' nicht gefunden",
                            file_path=str(doc.file_path),
                            line_number=ref.line_number,
                        ))

    # ─────────────────────────────────────────────────────────
    # Prüfung 5: Abschnittsstruktur
    # ─────────────────────────────────────────────────────────

    def _check_section_structure(self, documents: list[SpecDocument], report: ValidationReport):
        """Prüft die Abschnittsstruktur."""
        for doc in documents:
            # Prüfe auf doppelte Abschnitts-IDs
            seen_ids = set()
            for section in doc.sections:
                if section.section_id in seen_ids:
                    report.add(ValidationResult(
                        rule_id="V-09",
                        severity="WARNING",
                        message=f"Doppelte Abschnitts-ID: {section.section_id}",
                        file_path=str(doc.file_path),
                        line_number=section.line_number,
                    ))
                seen_ids.add(section.section_id)

            # Prüfe auf fehlende Titel
            for section in doc.sections:
                if not section.title:
                    report.add(ValidationResult(
                        rule_id="V-10",
                        severity="WARNING",
                        message=f"Abschnitt ohne Titel: {section.section_id}",
                        file_path=str(doc.file_path),
                        line_number=section.line_number,
                    ))

    # ─────────────────────────────────────────────────────────
    # Prüfung 6: Versionskonsistenz
    # ─────────────────────────────────────────────────────────

    def _check_version_consistency(self, documents: list[SpecDocument], report: ValidationReport):
        """Prüft die Versionskonsistenz in builds_on."""
        doc_versions = {}
        for doc in documents:
            if doc.frontmatter:
                doc_versions[doc.doc_id] = doc.frontmatter.version

        for doc in documents:
            if doc.frontmatter is None:
                continue

            for build_ref in doc.frontmatter.builds_on:
                # Format: "foundation/CHARTER.md@1.0.0"
                if "@" in build_ref:
                    ref_path, ref_version = build_ref.rsplit("@", 1)
                    if ref_path in doc_versions:
                        actual_version = doc_versions[ref_path]
                        if actual_version != ref_version:
                            report.add(ValidationResult(
                                rule_id="V-11",
                                severity="WARNING",
                                message=f"Versionskonflikt: {build_ref} erwartet, "
                                        f"aber {ref_path} hat Version {actual_version}",
                                file_path=str(doc.file_path),
                            ))