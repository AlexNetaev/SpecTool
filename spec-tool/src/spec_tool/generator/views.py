"""
View-Generator für Spezifikationsdokumente.
Erzeugt rollenzentrierte Sichten, Datenfluss-Karten und Test-Matrizen.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime

from spec_tool.models import (
    SpecDocument,
    Section,
    SectionType,
    ParsedTable,
    Reference,
)


@dataclass
class RoleView:
    """Rollenzentrierte Sicht auf eine Rolle."""
    role_id: str
    display_name: str = ""
    layer: Optional[int] = None
    uses_llm: bool = False
    pipeline_stage: Optional[str] = None
    permissions_allowed: list[str] = field(default_factory=list)
    permissions_forbidden: list[str] = field(default_factory=list)
    inputs: list[dict] = field(default_factory=list)
    outputs: list[dict] = field(default_factory=list)
    rules: list[dict] = field(default_factory=list)
    dataflows: list[str] = field(default_factory=list)
    tests: list[str] = field(default_factory=list)
    source_file: str = ""


@dataclass
class DataflowView:
    """Datenfluss-Sicht."""
    dataflow_id: str
    trigger: str = ""
    source_role: str = ""
    target_role: str = ""
    steps: list[str] = field(default_factory=list)
    source_file: str = ""


@dataclass
class TestMatrixEntry:
    """Eintrag in der Test-Matrix."""
    test_id: str
    test_name: str
    expected: str
    role: str = ""
    source_file: str = ""


def _iter_sections_recursive(sections: List[Section]):
    """Rekursiver Iterator über alle Abschnitte."""
    for section in sections:
        yield section
        if section.children:
            yield from _iter_sections_recursive(section.children)


class ViewGenerator:
    """
    Generiert Sichten aus geparsten Spezifikationsdokumenten.
    """

    def generate_role_views(self, documents: list[SpecDocument]) -> list[RoleView]:
        """Generiert rollenzentrierte Sichten aus allen Dokumenten."""
        roles: dict[str, RoleView] = {}

        for doc in documents:
            # Rekursiv durch alle Abschnitte iterieren
            for section in _iter_sections_recursive(doc.sections):
                if section.section_type == SectionType.ROLE_DEFINITION and section.role_id:
                    role_id = section.role_id

                    if role_id not in roles:
                        roles[role_id] = RoleView(
                            role_id=role_id,
                            display_name=section.title,
                            layer=section.role_layer,
                            uses_llm=section.role_llm or False,
                            source_file=str(doc.file_path),
                        )

                    role = roles[role_id]

                    # Tabellen extrahieren
                    for table in section.tables:
                        self._extract_role_table(role, table)

                    # Datenflüsse in Kind-Abschnitten extrahieren
                    for child in section.children:
                        if child.section_type == SectionType.DATAFLOW and child.dataflow_id:
                            role.dataflows.append(child.dataflow_id)

        return list(roles.values())

    def _extract_role_table(self, role: RoleView, table: ParsedTable):
        """Extrahiert Rollen-Informationen aus einer Tabelle."""
        schema = table.schema_name or ""

        if schema == "role_permissions":
            for row in table.rows:
                if len(row) >= 2:
                    allowed = row[0].strip()
                    forbidden = row[1].strip() if len(row) > 1 else ""
                    if allowed and allowed != "Erlaubt":
                        role.permissions_allowed.append(allowed)
                    if forbidden and forbidden != "Verboten":
                        role.permissions_forbidden.append(forbidden)

        elif schema == "role_inputs":
            for row in table.rows:
                if len(row) >= 4 and row[0] != "Quelle":
                    role.inputs.append({
                        "quelle": row[0],
                        "daten": row[1],
                        "vertrag": row[2],
                        "bedingung": row[3],
                    })

        elif schema == "role_outputs":
            for row in table.rows:
                if len(row) >= 4 and row[0] != "Ziel":
                    role.outputs.append({
                        "ziel": row[0],
                        "daten": row[1],
                        "vertrag": row[2],
                        "bedingung": row[3],
                    })

        elif schema == "role_rules":
            for row in table.rows:
                if len(row) >= 3 and row[0] != "Regel":
                    role.rules.append({
                        "regel": row[0],
                        "charter_ref": row[1],
                        "konsequenz": row[2],
                    })

    def generate_dataflow_views(self, documents: list[SpecDocument]) -> list[DataflowView]:
        """Generiert Datenfluss-Sichten aus allen Dokumenten."""
        dataflows: list[DataflowView] = []

        for doc in documents:
            for section in _iter_sections_recursive(doc.sections):
                if section.section_type == SectionType.DATAFLOW and section.dataflow_id:
                    df = DataflowView(
                        dataflow_id=section.dataflow_id,
                        trigger=section.dataflow_trigger or "",
                        source_file=str(doc.file_path),
                    )

                    # Schritte extrahieren
                    for child in section.children:
                        if child.content.strip():
                            df.steps.append(child.content.strip())

                    dataflows.append(df)

        return dataflows

    def generate_test_matrix(self, documents: list[SpecDocument]) -> list[TestMatrixEntry]:
        """Generiert eine Test-Matrix aus allen Dokumenten."""
        entries: list[TestMatrixEntry] = []

        for doc in documents:
            for section in _iter_sections_recursive(doc.sections):
                if section.section_type == SectionType.TEST_SUITE:
                    for table in section.tables:
                        if table.schema_name == "test_cases":
                            for row in table.rows:
                                if len(row) >= 3 and row[0] != "Test-ID":
                                    entries.append(TestMatrixEntry(
                                        test_id=row[0],
                                        test_name=row[1],
                                        expected=row[2],
                                        role=row[4] if len(row) > 4 else "",
                                        source_file=str(doc.file_path),
                                    ))

        return entries

    def render_role_views_markdown(self, role_views: list) -> str:
        """Rendert Rollen-Views als Markdown."""
        lines = ["# 📋 Rollen-Views\n"]
        lines.append(f"Generiert: {datetime.now().isoformat()}\n")
        lines.append(f"Anzahl Rollen: {len(role_views)}\n\n")

        for role in role_views:
            lines.append(f"## {role.role_id}\n\n")
            lines.append(f"**Schicht:** {role.layer or '?'}\n")
            lines.append(f"**LLM:** {'Ja' if role.uses_llm else 'Nein'}\n\n")

            if role.inputs:
                lines.append("### Eingänge\n")
                for inp in role.inputs:
                    lines.append(f"- {inp}\n")
                lines.append("\n")

            if role.outputs:
                lines.append("### Ausgänge\n")
                for out in role.outputs:
                    lines.append(f"- {out}\n")
                lines.append("\n")

            if role.rules:
                lines.append("### Regeln\n")
                for rule in role.rules:
                    lines.append(f"- {rule}\n")
                lines.append("\n")

            lines.append("---\n\n")

        return "".join(lines)


    def render_dataflow_views_markdown(self, df_views: list) -> str:
        """Rendert Datenfluss-Views als Markdown."""
        lines = ["# 🔄 Datenfluss-Views\n"]
        lines.append(f"Generiert: {datetime.now().isoformat()}\n")
        lines.append(f"Anzahl Datenflüsse: {len(df_views)}\n\n")

        for df in df_views:
            lines.append(f"## {df.dataflow_id}\n\n")
            if df.trigger:
                lines.append(f"**Trigger:** {df.trigger}\n\n")

            if df.steps:
                lines.append("### Schritte\n")
                for i, step in enumerate(df.steps, 1):
                    lines.append(f"{i}. {step}\n")
                lines.append("\n")

            lines.append("---\n\n")

        return "".join(lines)


    def render_test_matrix_markdown(self, test_entries: list) -> str:
        """Rendert Test-Matrix als Markdown."""
        lines = ["# 🧪 Test-Matrix\n"]
        lines.append(f"Generiert: {datetime.now().isoformat()}\n")
        lines.append(f"Anzahl Test-Einträge: {len(test_entries)}\n\n")

        if not test_entries:
            lines.append("Keine Test-Einträge gefunden.\n")
            return "".join(lines)

        lines.append("| Test-ID | Typ | Beschreibung |\n")
        lines.append("|---------|-----|--------------|\n")

        for entry in test_entries:
            test_id = entry.get('test_id', 'N/A')
            test_type = entry.get('type', 'N/A')
            description = entry.get('description', 'N/A')
            lines.append(f"| {test_id} | {test_type} | {description} |\n")

        return "".join(lines)