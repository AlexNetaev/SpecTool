"""
Hauptparser für Spezifikationsdateien.
Liest eine MD-Datei und erzeugt ein SpecDocument-Objekt.

Version: 1.0.2
Fixes:
  - Windows-Zeilenenden (\r\n) werden normalisiert
  - @ref-Marker werden als Referenzen behandelt
  - @table-Marker werden den Tabellen zugeordnet
  - §-Abschnitte ohne #-Überschriften werden erkannt
  - llm-Attribut kann bool oder str sein
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


# ─────────────────────────────────────────────────────────────
# Regex-Patterns
# ─────────────────────────────────────────────────────────────

# Markdown-Überschriften (# bis ######)
HEADING_PATTERN = re.compile(r"^(#{1,6})\s+(.+)$", re.MULTILINE)

# §-Abschnittsnummern in Überschriften
SECTION_NUM_PATTERN = re.compile(r"§([\d]+(?:\.[\d]+)*)")

# §-Abschnitte OHNE #-Überschrift (z.B. "§1 Paket-Verträge" als reine Textzeile)
SECTION_LINE_PATTERN = re.compile(r"^§([\d]+(?:\.[\d]+)*)\s+(.+)$")

# Nummerierte Abschnitte ohne § (z.B. "0. Geltung und Änderungsregeln")
NUMBERED_SECTION_PATTERN = re.compile(r"^(\d+)\.\s+(.+)$")

# Tabellen-Erkennung
TABLE_ROW_PATTERN = re.compile(r"^\|(.+)\|$")
TABLE_SEPARATOR_PATTERN = re.compile(r"^\|[\s\-:|]+\|$")

# Querverweise im Fließtext
REF_PATTERN = re.compile(
    r"→\s*(?:Siehe\s+)?(?:`)?([\w/\.]+)(?:\s*§([\d]+(?:\.[\d]+)*|SR-[\d]+))?(?:`)?",
)

# CHARTER-Referenzen
CHARTER_REF_PATTERN = re.compile(
    r"CHARTER\s*§(SR-[\d]+)",
)

# Bekannte Dokument-Abkürzungen
KNOWN_DOCS = {
    "CHARTER": "foundation/CHARTER.md",
    "CONTRACTS": "foundation/CONTRACTS.md",
    "SPEC_FORMAT": "foundation/SPEC_FORMAT.md",
    "MASTER_INDEX": "foundation/MASTER_INDEX.md",
    "QUESTOR": "specs/QUESTOR.md",
    "HAL": "specs/HAL.md",
    "GREMIUM": "specs/GREMIUM.md",
    "GREMIUM_STRATEGY": "specs/GREMIUM_STRATEGY.md",
    "CAROUSEL_TWIN": "specs/CAROUSEL_TWIN.md",
    "VALIDATION": "ops/VALIDATION.md",
    "VALIDATION_ATLAS": "ops/VALIDATION_ATLAS.md",
    "ROADMAP": "ops/ROADMAP.md",
}


# ─────────────────────────────────────────────────────────────
# Parser-Klasse
# ─────────────────────────────────────────────────────────────

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

    def parse_content(
        self,
        content: str,
        file_path: Optional[Path] = None,
    ) -> SpecDocument:
        """Parst den Inhalt einer Spezifikationsdatei."""
        if file_path is None:
            file_path = Path("unknown.md")

        errors: list[str] = []

        # ── FIX: Windows-Zeilenenden normalisieren ──
        content = content.replace("\r\n", "\n").replace("\r", "\n")

        # 1. Frontmatter parsen
        frontmatter, body = parse_frontmatter(content)
        if frontmatter is None:
            errors.append("Kein gültiger YAML-Frontmatter gefunden")

        # 2. Marker aus dem BODY parsen
        markers = parse_markers_multiline(body)

        # 3. Abschnitte parsen
        sections = self._parse_sections(body, markers)

        # 4. Tabellen parsen (mit @table-Marker-Zuordnung)
        tables = self._parse_tables(body, markers)

        # 5. Querverweise parsen (inkl. @ref-Marker)
        references = self._parse_references(body, str(file_path), markers)

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
    ) -> list[Section]:
        """
        Parst Abschnitte aus dem Inhalt.

        Erkennt drei Arten von Abschnitts-Überschriften:
        1. Markdown-Überschriften: ## §1 Titel
        2. §-Textzeilen: §1 Titel (ohne #)
        3. Nummerierte Textzeilen: 1. Titel (ohne § und #)
        """
        sections: list[Section] = []
        current_section: Optional[Section] = None
        section_stack: list[Section] = []

        lines = body.split("\n")
        line_num = 0

        for line in lines:
            line_num += 1
            stripped = line.strip()

            # ── 1. Markdown-Überschrift erkennen ──
            heading_match = HEADING_PATTERN.match(stripped)
            if heading_match:
                level = len(heading_match.group(1))
                title = heading_match.group(2).strip()

                section_num_match = SECTION_NUM_PATTERN.search(title)
                section_id = (
                    section_num_match.group(1)
                    if section_num_match
                    else f"auto-{line_num}"
                )

                section_type = self._determine_section_type(markers, line_num)

                new_section = Section(
                    section_id=section_id,
                    title=title,
                    section_type=section_type,
                    level=level,
                    line_number=line_num,
                )

                self._apply_marker_attributes(new_section, markers, line_num)
                self._insert_section(
                    new_section, level, sections, section_stack
                )
                current_section = new_section
                continue

            # ── 2. §-Textzeile ohne #-Überschrift erkennen ──
            section_line_match = SECTION_LINE_PATTERN.match(stripped)
            if section_line_match:
                section_id = section_line_match.group(1)
                title = stripped

                section_type = self._determine_section_type(markers, line_num)

                new_section = Section(
                    section_id=section_id,
                    title=title,
                    section_type=section_type,
                    level=2,
                    line_number=line_num,
                )

                self._apply_marker_attributes(new_section, markers, line_num)
                self._insert_section(new_section, 2, sections, section_stack)
                current_section = new_section
                continue

            # ── 3. Nummerierte Textzeile ohne § erkennen ──
            numbered_match = NUMBERED_SECTION_PATTERN.match(stripped)
            if numbered_match:
                # Nur als Abschnitt behandeln, wenn die Zeile kurz ist
                # (verhindert, dass normale Listen als Abschnitte gelten)
                if len(stripped) < 120:
                    section_id = numbered_match.group(1)
                    title = stripped

                    section_type = self._determine_section_type(
                        markers, line_num
                    )

                    new_section = Section(
                        section_id=section_id,
                        title=title,
                        section_type=section_type,
                        level=2,
                        line_number=line_num,
                    )

                    self._apply_marker_attributes(
                        new_section, markers, line_num
                    )
                    self._insert_section(
                        new_section, 2, sections, section_stack
                    )
                    current_section = new_section
                    continue

            # ── 4. Inhalt zum aktuellen Abschnitt hinzufügen ──
            if current_section is not None:
                current_section.content += line + "\n"

        return sections

    def _insert_section(
        self,
        new_section: Section,
        level: int,
        sections: list[Section],
        section_stack: list[Section],
    ) -> None:
        """Fügt einen Abschnitt in die Hierarchie ein."""
        if level == 1:
            sections.append(new_section)
            section_stack.clear()
            section_stack.append(new_section)
        else:
            while section_stack and section_stack[-1].level >= level:
                section_stack.pop()

            if section_stack:
                section_stack[-1].children.append(new_section)
            else:
                sections.append(new_section)

            section_stack.append(new_section)

    def _determine_section_type(
        self,
        markers: list[Marker],
        line_num: int,
    ) -> SectionType:
        """Bestimmt den Section-Typ basierend auf Markern in der Nähe."""
        for marker in markers:
            if marker.marker_type == MarkerType.SECTION:
                if abs(marker.line_number - line_num) <= 5:
                    type_str = marker.attributes.get("type", "prose")
                    try:
                        return SectionType(type_str)
                    except ValueError:
                        return SectionType.PROSE
        return SectionType.PROSE

    def _apply_marker_attributes(
        self,
        section: Section,
        markers: list[Marker],
        line_num: int,
    ) -> None:
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

                layer_val = marker.attributes.get("layer")
                if layer_val is not None:
                    try:
                        section.role_layer = int(layer_val)
                    except (ValueError, TypeError):
                        pass

                # ── FIX: llm kann bool oder str sein ──
                llm_val = marker.attributes.get("llm")
                if llm_val is not None:
                    if isinstance(llm_val, bool):
                        section.role_llm = llm_val
                    elif isinstance(llm_val, str):
                        section.role_llm = llm_val.lower() == "true"

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

    def _parse_tables(
        self,
        body: str,
        markers: list[Marker] = None,
    ) -> list[ParsedTable]:
        """
        Parst alle Markdown-Tabellen und verknüpft sie mit @table-Markern.
        """
        tables: list[ParsedTable] = []
        lines = body.split("\n")

        # @table-Marker nach Zeilennummer sammeln
        table_markers: dict[int, str] = {}
        if markers:
            for m in markers:
                if m.marker_type == MarkerType.TABLE:
                    schema = m.attributes.get("schema")
                    if schema:
                        table_markers[m.line_number] = schema

        i = 0
        while i < len(lines):
            line = lines[i].strip()

            if TABLE_ROW_PATTERN.match(line) and i + 1 < len(lines):
                next_line = lines[i + 1].strip()
                if TABLE_SEPARATOR_PATTERN.match(next_line):
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

                    # ── FIX: @table-Marker zuordnen ──
                    # Der @table-Marker steht direkt vor der Tabelle.
                    # Wir suchen rückwärts in den letzten 5 Zeilen.
                    schema_name = None
                    table_line = i + 1  # 1-basiert
                    for marker_line, schema in table_markers.items():
                        if 0 <= (table_line - marker_line) <= 5:
                            schema_name = schema
                            break

                    tables.append(
                        ParsedTable(
                            schema_name=schema_name,
                            headers=headers,
                            rows=rows,
                            line_number=i + 1,
                        )
                    )
                    i = j
                    continue

            i += 1

        return tables

    def _parse_table_row(self, line: str) -> list[str]:
        """Parst eine einzelne Tabellenzeile."""
        line = line.strip()
        if line.startswith("|"):
            line = line[1:]
        if line.endswith("|"):
            line = line[:-1]
        return [cell.strip() for cell in line.split("|")]

    # ─────────────────────────────────────────────────────────
    # Intern: Querverweise
    # ─────────────────────────────────────────────────────────

    def _parse_references(
        self,
        body: str,
        source_doc: str,
        markers: list[Marker] = None,
    ) -> list[Reference]:
        """
        Parst alle Querverweise aus dem Inhalt UND aus @ref-Markern.
        """
        references: list[Reference] = []
        lines = body.split("\n")

        # ── FIX: @ref-Marker als Referenzen behandeln ──
        if markers:
            for m in markers:
                if m.marker_type == MarkerType.REF:
                    target = m.attributes.get("target", "")
                    ref_type_str = m.attributes.get("type", "spec")

                    target_doc = target
                    target_section = None

                    if "§" in target:
                        parts = target.split("§", 1)
                        target_doc = parts[0].strip()
                        target_section = parts[1].strip()

                    target_doc = self._resolve_target_doc(target_doc)

                    try:
                        ref_type = ReferenceType(ref_type_str)
                    except ValueError:
                        ref_type = ReferenceType.SPEC

                    references.append(
                        Reference(
                            source_doc=source_doc,
                            target_doc=target_doc,
                            target_section=target_section,
                            reference_type=ref_type,
                            raw_text=m.raw,
                            line_number=m.line_number,
                        )
                    )

        # ── Text-basierte Referenz-Erkennung ──
        for line_num, line in enumerate(lines, start=1):
            # CHARTER-Referenzen
            for match in CHARTER_REF_PATTERN.finditer(line):
                sr_id = match.group(1)
                references.append(
                    Reference(
                        source_doc=source_doc,
                        target_doc="foundation/CHARTER.md",
                        target_section=sr_id,
                        reference_type=ReferenceType.SECURITY_RULE,
                        raw_text=match.group(0),
                        line_number=line_num,
                    )
                )

            # Allgemeine Referenzen (→ CONTRACTS §X.X)
            for match in REF_PATTERN.finditer(line):
                target = match.group(1)
                section = match.group(2)

                target_doc = self._resolve_target_doc(target)

                references.append(
                    Reference(
                        source_doc=source_doc,
                        target_doc=target_doc,
                        target_section=section,
                        reference_type=self._determine_reference_type(target),
                        raw_text=match.group(0),
                        line_number=line_num,
                    )
                )

        # ── Duplikate entfernen ──
        seen: set[tuple] = set()
        unique_refs: list[Reference] = []
        for ref in references:
            key = (
                ref.source_doc,
                ref.target_doc,
                ref.target_section,
                ref.line_number,
            )
            if key not in seen:
                seen.add(key)
                unique_refs.append(ref)

        return unique_refs

    def _resolve_target_doc(self, target: str) -> str:
        """Löst das Ziel-Dokument aus einer Referenz auf."""
        target = target.strip()

        # Bereits vollständiger Pfad
        if "/" in target:
            return target

        # Bekannte Abkürzungen
        return KNOWN_DOCS.get(target, target)

    def _determine_reference_type(self, target: str) -> ReferenceType:
        """Bestimmt den Referenztyp basierend auf dem Ziel."""
        if "CHARTER" in target or "SR-" in target:
            return ReferenceType.SECURITY_RULE
        elif "CONTRACTS" in target:
            return ReferenceType.CONTRACT
        elif ".md" in target or "SPEC" in target:
            return ReferenceType.SPEC
        return ReferenceType.SPEC

    # ─────────────────────────────────────────────────────────
    # Intern: Zuordnung
    # ─────────────────────────────────────────────────────────

    def _assign_references_to_sections(
        self,
        sections: list[Section],
        references: list[Reference],
    ) -> None:
        """Ordnet Querverweise den Abschnitten zu."""
        for ref in references:
            best_section = None
            best_distance = float("inf")

            for section in sections:
                distance = abs(section.line_number - ref.line_number)
                if distance < best_distance:
                    best_distance = distance
                    best_section = section

            if best_section is not None and best_distance <= 50:
                best_section.references.append(ref)

    def _assign_markers_to_sections(
        self,
        sections: list[Section],
        markers: list[Marker],
    ) -> None:
        """Ordnet Marker den Abschnitten zu."""
        for marker in markers:
            best_section = None
            best_distance = float("inf")

            for section in sections:
                distance = abs(section.line_number - marker.line_number)
                if distance < best_distance:
                    best_distance = distance
                    best_section = section

            if best_section is not None and best_distance <= 10:
                best_section.markers.append(marker)