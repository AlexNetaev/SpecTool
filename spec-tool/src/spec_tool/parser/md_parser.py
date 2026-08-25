"""
Hauptparser für Spezifikationsdateien.
Liest eine MD-Datei und erzeugt ein SpecDocument-Objekt.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Optional

from spec_tool.models import (
    SpecDocument,
    Section,
    SectionType,
    ParsedTable,
    Reference,
    ReferenceType,
    Marker,
    MarkerType,
)
from spec_tool.parser.frontmatter import parse_frontmatter
from spec_tool.parser.markers import parse_markers_multiline


# Regex für Markdown-Überschriften
HEADING_PATTERN = re.compile(r"^(#{1,6})\s+(.+)$", re.MULTILINE)

# Regex für §-Abschnittsnummern in Überschriften
SECTION_NUM_PATTERN = re.compile(r"§([\d]+(?:\.[\d]+)*)")

# Regex für Tabellen
TABLE_ROW_PATTERN = re.compile(r"^\|(.+)\|$")
TABLE_SEPARATOR_PATTERN = re.compile(r"^\|[\s\-:|]+\|$")

# Regex für Querverweise im Text
REF_PATTERN = re.compile(
    r"→\s*(?:Siehe\s+)?(?:`)?([\w/\.]+)(?:§([\d]+(?:\.[\d]+)*))?(?:`)?",
)

# Regex für CHARTER-Referenzen
CHARTER_REF_PATTERN = re.compile(
    r"CHARTER\s*§(SR-[\d]+)",
)


class MarkdownParser:
    """
    Parser für Spezifikationsdateien im SPEC_FORMAT.

    Verwendung:
        parser = MarkdownParser()
        doc = parser.parse_file(Path("foundation/CHARTER.md"))
    """

    def parse_file(self, file_path: Path) -> SpecDocument:
        """Parst eine Spezifikationsdatei und gibt ein SpecDocument zurück."""
        content = file_path.read_text(encoding="utf-8")
        return self.parse_content(content, file_path)

    def parse_content(self, content: str, file_path: Optional[Path] = None) -> SpecDocument:
        """Parst den Inhalt einer Spezifikationsdatei."""
        if file_path is None:
            file_path = Path("unknown.md")

        errors: list[str] = []

        # 1. Frontmatter parsen
        frontmatter, body = parse_frontmatter(content)
        if frontmatter is None:
            errors.append("Kein gültiger YAML-Frontmatter gefunden")

        # 2. Marker parsen
        markers = parse_markers_multiline(content)

        # 3. Abschnitte parsen
        sections = self._parse_sections(body, markers, file_path, errors)

        # 4. Tabellen parsen
        tables = self._parse_tables(body)

        # 5. Querverweise parsen
        references = self._parse_references(body, str(file_path))

        # 6. Referenzen den Abschnitten zuordnen
        self._assign_references_to_sections(sections, references)

        # 7. Marker den Abschnitten zuordnen
        self._assign_markers_to_sections(sections, markers)

        return SpecDocument(
            file_path=file_path,
            frontmatter=frontmatter,
            sections=sections,
            references=references,
            markers=markers,
            tables=tables,
            raw_content=content,
            parse_errors=errors,
        )

    # ─────────────────────────────────────────────────────────
    # Intern: Abschnitte
    # ─────────────────────────────────────────────────────────

    def _parse_sections(
        self,
        body: str,
        markers: list[Marker],
        file_path: Path,
        errors: list[str],
    ) -> list[Section]:
        """Parst Abschnitte aus dem Inhalt."""
        sections: list[Section] = []
        current_section: Optional[Section] = None
        section_stack: list[Section] = []

        lines = body.split("\n")
        line_num = 0

        for line in lines:
            line_num += 1

            # Überschrift erkennen
            heading_match = HEADING_PATTERN.match(line)
            if heading_match:
                level = len(heading_match.group(1))
                title = heading_match.group(2).strip()

                # Abschnittsnummer extrahieren
                section_num_match = SECTION_NUM_PATTERN.search(title)
                section_id = section_num_match.group(1) if section_num_match else f"auto-{line_num}"

                # Section-Typ aus Markern bestimmen
                section_type = self._determine_section_type(markers, line_num)

                new_section = Section(
                    section_id=section_id,
                    title=title,
                    section_type=section_type,
                    level=level,
                    line_number=line_num,
                )

                # Rollen-Attribute aus Markern übernehmen
                self._apply_marker_attributes(new_section, markers, line_num)

                # Hierarchie aufbauen
                if level == 1:
                    sections.append(new_section)
                    section_stack = [new_section]
                else:
                    # Parent finden
                    while section_stack and section_stack[-1].level >= level:
                        section_stack.pop()

                    if section_stack:
                        section_stack[-1].children.append(new_section)
                    else:
                        sections.append(new_section)

                    section_stack.append(new_section)

                current_section = new_section

            elif current_section is not None:
                # Inhalt zum aktuellen Abschnitt hinzufügen
                current_section.content += line + "\n"

        return sections

    def _determine_section_type(self, markers: list[Marker], line_num: int) -> SectionType:
        """Bestimmt den Section-Typ basierend auf Markern in der Nähe."""
        for marker in markers:
            if marker.marker_type == MarkerType.SECTION:
                # Marker in der Nähe der Überschrift (±3 Zeilen)
                if abs(marker.line_number - line_num) <= 3:
                    type_str = marker.attributes.get("type", "prose")
                    try:
                        return SectionType(type_str)
                    except ValueError:
                        return SectionType.PROSE
        return SectionType.PROSE

    def _apply_marker_attributes(self, section: Section, markers: list[Marker], line_num: int):
        """Übernimmt Attribute von Markern in der Nähe der Überschrift."""
        for marker in markers:
            if abs(marker.line_number - line_num) > 5:
                continue

            if marker.marker_type == MarkerType.SECTION:
                section.role_id = marker.attributes.get("role")
                section.contract_name = marker.attributes.get("contract")
                section.dataflow_id = marker.attributes.get("dataflow")

            elif marker.marker_type == MarkerType.ROLE:
                section.section_type = SectionType.ROLE_DEFINITION
                section.role_id = marker.attributes.get("id")
                layer_str = marker.attributes.get("layer")
                if layer_str:
                    try:
                        section.role_layer = int(layer_str)
                    except ValueError:
                        pass
                llm_str = marker.attributes.get("llm")
                if llm_str:
                    section.role_llm = llm_str.lower() == "true"

            elif marker.marker_type == MarkerType.CONTRACT:
                section.section_type = SectionType.CONTRACT
                section.contract_name = marker.attributes.get("name")
                section.contract_type = marker.attributes.get("type")

            elif marker.marker_type == MarkerType.DATAFLOW:
                section.section_type = SectionType.DATAFLOW
                section.dataflow_id = marker.attributes.get("id")
                section.dataflow_trigger = marker.attributes.get("trigger")

            elif marker.marker_type == MarkerType.SAFETY_RULE:
                section.section_type = SectionType.SAFETY_RULE
                section.safety_rule_id = marker.attributes.get("id")

    # ─────────────────────────────────────────────────────────
    # Intern: Tabellen
    # ─────────────────────────────────────────────────────────

    def _parse_tables(self, body: str) -> list[ParsedTable]:
        """Parst alle Markdown-Tabellen aus dem Inhalt."""
        tables: list[ParsedTable] = []
        lines = body.split("\n")
        i = 0

        while i < len(lines):
            line = lines[i].strip()

            # Tabellen-Header erkennen
            if TABLE_ROW_PATTERN.match(line) and i + 1 < len(lines):
                next_line = lines[i + 1].strip()
                if TABLE_SEPARATOR_PATTERN.match(next_line):
                    # Tabelle gefunden
                    headers = self._parse_table_row(line)
                    rows: list[list[str]] = []
                    j = i + 2

                    while j < len(lines):
                        row_line = lines[j].strip()
                        if TABLE_ROW_PATTERN.match(row_line):
                            rows.append(self._parse_table_row(row_line))
                            j += 1
                        else:
                            break

                    tables.append(ParsedTable(
                        headers=headers,
                        rows=rows,
                        line_number=i + 1,
                    ))
                    i = j
                    continue

            i += 1

        return tables

    def _parse_table_row(self, line: str) -> list[str]:
        """Parst eine einzelne Tabellenzeile."""
        # Pipe-Zeichen am Anfang und Ende entfernen
        line = line.strip()
        if line.startswith("|"):
            line = line[1:]
        if line.endswith("|"):
            line = line[:-1]
        return [cell.strip() for cell in line.split("|")]

    # ─────────────────────────────────────────────────────────
    # Intern: Querverweise
    # ─────────────────────────────────────────────────────────

    def _parse_references(self, body: str, source_doc: str) -> list[Reference]:
        """Parst alle Querverweise aus dem Inhalt."""
        references: list[Reference] = []
        lines = body.split("\n")

        for line_num, line in enumerate(lines, start=1):
            # CHARTER-Referenzen
            for match in CHARTER_REF_PATTERN.finditer(line):
                sr_id = match.group(1)
                references.append(Reference(
                    source_doc=source_doc,
                    target_doc="foundation/CHARTER.md",
                    target_section=f"SR-{sr_id.split('-')[1]}" if "-" in sr_id else sr_id,
                    reference_type=ReferenceType.SECURITY_RULE,
                    raw_text=match.group(0),
                    line_number=line_num,
                ))

            # Allgemeine Referenzen (→ CONTRACTS §X.X)
            for match in REF_PATTERN.finditer(line):
                target = match.group(1)
                section = match.group(2)

                # Ziel-Dokument bestimmen
                target_doc = self._resolve_target_doc(target, source_doc)

                references.append(Reference(
                    source_doc=source_doc,
                    target_doc=target_doc,
                    target_section=section,
                    reference_type=self._determine_reference_type(target),
                    raw_text=match.group(0),
                    line_number=line_num,
                ))

        return references

    def _resolve_target_doc(self, target: str, source_doc: str) -> str:
        """Löst das Ziel-Dokument aus einer Referenz auf."""
        target = target.strip()

        # Bereits vollständiger Pfad
        if "/" in target:
            return target

        # Bekannte Abkürzungen
        known_docs = {
            "CHARTER": "foundation/CHARTER.md",
            "CONTRACTS": "foundation/CONTRACTS.md",
            "QUESTOR": "specs/QUESTOR.md",
            "HAL": "specs/HAL.md",
            "GREMIUM": "specs/GREMIUM.md",
            "GREMIUM_STRATEGY": "specs/GREMIUM_STRATEGY.md",
            "CAROUSEL_TWIN": "specs/CAROUSEL_TWIN.md",
            "VALIDATION": "ops/VALIDATION.md",
            "VALIDATION_ATLAS": "ops/VALIDATION_ATLAS.md",
            "ROADMAP": "ops/ROADMAP.md",
        }

        return known_docs.get(target, target)

    def _determine_reference_type(self, target: str) -> ReferenceType:
        """Bestimmt den Referenztyp basierend auf dem Ziel."""
        if "CHARTER" in target or "SR-" in target:
            return ReferenceType.SECURITY_RULE
        elif "CONTRACTS" in target:
            return ReferenceType.CONTRACT
        elif "SPEC" in target or ".md" in target:
            return ReferenceType.SPEC
        return ReferenceType.SPEC

    # ─────────────────────────────────────────────────────────
    # Intern: Zuordnung
    # ─────────────────────────────────────────────────────────

    def _assign_references_to_sections(self, sections: list[Section], references: list[Reference]):
        """Ordnet Querverweise den Abschnitten zu."""
        for ref in references:
            for section in sections:
                if self._reference_in_section(ref, section):
                    section.references.append(ref)
                    break

    def _reference_in_section(self, ref: Reference, section: Section) -> bool:
        """Prüft, ob ein Querverweis in einem Abschnitt liegt."""
        # Vereinfacht: Zeilennummer vergleichen
        return section.line_number <= ref.line_number

    def _assign_markers_to_sections(self, sections: list[Section], markers: list[Marker]):
        """Ordnet Marker den Abschnitten zu."""
        for marker in markers:
            for section in sections:
                if abs(marker.line_number - section.line_number) <= 5:
                    section.markers.append(marker)
                    break