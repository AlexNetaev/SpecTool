"""
View-Generator für Spezifikationsdokumente.
Erzeugt rollenzentrierte Sichten, Datenfluss-Karten und Test-Matrizen.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

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


class ViewGenerator:
    """
    Generiert Sichten aus geparsten Spezifikationsdokumenten.

    Verwendung:
        generator = ViewGenerator()
        role_views = generator.generate_role_views(documents)
        dataflow_views = generator.generate_dataflow_views(documents)
        test_matrix = generator.generate_test_matrix(documents)
    """

    # ─────────────────────────────────────────────────────────
    # Rollen-Views
    # ─────────────────────────────────────────────────────────

    def generate_role_views(self, documents: list[SpecDocument]) -> list[RoleView]:
        """Generiert rollenzentrierte Sichten aus allen Dokumenten."""
        roles: dict[str, RoleView] = {}

        for doc in documents:
            for section in doc.sections:
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

                    # Datenflüsse extrahieren
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

    def render_role_views_markdown(self, roles: list[RoleView]) -> str:
        """Rendert die Rollen-Views als Markdown."""
        lines = [
            "# 📋 ROLE_VIEWS — Rollenzentrierte Sichten",
            "",
            f"*Automatisch generiert aus {len(roles)} Rollen.*",
            "",
        ]

        for role in roles:
            lines.append(f"## {role.display_name or role.role_id}")
            lines.append("")

            if role.layer is not None:
                lines.append(f"- **Schicht:** {role.layer}")
            if role.uses_llm:
                lines.append("- **LLM:** Ja")
            else:
                lines.append("- **LLM:** Nein")
            if role.pipeline_stage:
                lines.append(f"- **Pipeline-Stufe:** {role.pipeline_stage}")
            lines.append(f"- **Quelldatei:** `{role.source_file}`")
            lines.append("")

            if role.permissions_allowed:
                lines.append("### Erlaubt")
                lines.append("")
                for p in role.permissions_allowed:
                    lines.append(f"- {p}")
                lines.append("")

            if role.permissions_forbidden:
                lines.append("### Verboten")
                lines.append("")
                for p in role.permissions_forbidden:
                    lines.append(f"- {p}")
                lines.append("")

            if role.inputs:
                lines.append("### Eingänge")
                lines.append("")
                lines.append("| Quelle | Daten | Vertrag | Bedingung |")
                lines.append("|--------|-------|---------|-----------|")
                for inp in role.inputs:
                    lines.append(f"| {inp['quelle']} | {inp['daten']} | {inp['vertrag']} | {inp['bedingung']} |")
                lines.append("")

            if role.outputs:
                lines.append("### Ausgänge")
                lines.append("")
                lines.append("| Ziel | Daten | Vertrag | Bedingung |")
                lines.append("|------|-------|---------|-----------|")
                for out in role.outputs:
                    lines.append(f"| {out['ziel']} | {out['daten']} | {out['vertrag']} | {out['bedingung']} |")
                lines.append("")

            if role.rules:
                lines.append("### Regeln")
                lines.append("")
                lines.append("| Regel | CHARTER-Ref | Konsequenz |")
                lines.append("|-------|-------------|------------|")
                for rule in role.rules:
                    lines.append(f"| {rule['regel']} | {rule['charter_ref']} | {rule['konsequenz']} |")
                lines.append("")

            if role.dataflows:
                lines.append("### Datenflüsse")
                lines.append("")
                for df in role.dataflows:
                    lines.append(f"- `{df}`")
                lines.append("")

            if role.tests:
                lines.append("### Tests")
                lines.append("")
                for t in role.tests:
                    lines.append(f"- {t}")
                lines.append("")

            lines.append("---")
            lines.append("")

        return "\n".join(lines)

    # ─────────────────────────────────────────────────────────
    # Datenfluss-Views
    # ─────────────────────────────────────────────────────────

    def generate_dataflow_views(self, documents: list[SpecDocument]) -> list[DataflowView]:
        """Generiert Datenfluss-Sichten aus allen Dokumenten."""
        dataflows: list[DataflowView] = []

        for doc in documents:
            for section in doc.sections:
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

    def render_dataflow_views_markdown(self, dataflows: list[DataflowView]) -> str:
        """Rendert die Datenfluss-Views als Markdown."""
        lines = [
            "# 🔄 DATAFLOW_MAP — Datenfluss-Karte",
            "",
            f"*Automatisch generiert aus {len(dataflows)} Datenflüssen.*",
            "",
        ]

        for df in dataflows:
            lines.append(f"## `{df.dataflow_id}`")
            lines.append("")
            if df.trigger:
                lines.append(f"- **Trigger:** {df.trigger}")
            if df.source_role:
                lines.append(f"- **Von:** {df.source_role}")
            if df.target_role:
                lines.append(f"- **Nach:** {df.target_role}")
            lines.append(f"- **Quelldatei:** `{df.source_file}`")
            lines.append("")

            if df.steps:
                lines.append("### Schritte")
                lines.append("")
                for i, step in enumerate(df.steps, 1):
                    lines.append(f"{i}. {step}")
                lines.append("")

            lines.append("---")
            lines.append("")

        return "\n".join(lines)

    # ─────────────────────────────────────────────────────────
    # Test-Matrix
    # ─────────────────────────────────────────────────────────

    def generate_test_matrix(self, documents: list[SpecDocument]) -> list[TestMatrixEntry]:
        """Generiert eine Test-Matrix aus allen Dokumenten."""
        entries: list[TestMatrixEntry] = []

        for doc in documents:
            for section in doc.sections:
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

    def render_test_matrix_markdown(self, entries: list[TestMatrixEntry]) -> str:
        """Rendert die Test-Matrix als Markdown."""
        lines = [
            "# 🧪 TEST_MATRIX — Test-Matrix nach Rollen",
            "",
            f"*Automatisch generiert aus {len(entries)} Tests.*",
            "",
        ]

        # Nach Rollen gruppieren
        by_role: dict[str, list[TestMatrixEntry]] = {}
        for entry in entries:
            role = entry.role or "Unbekannt"
            if role not in by_role:
                by_role[role] = []
            by_role[role].append(entry)

        for role, role_entries in sorted(by_role.items()):
            lines.append(f"## {role}")
            lines.append("")
            lines.append("| Test-ID | Test | Erwartet |")
            lines.append("|---------|------|----------|")
            for entry in role_entries:
                lines.append(f"| {entry.test_id} | {entry.test_name} | {entry.expected} |")
            lines.append("")

        return "\n".join(lines)