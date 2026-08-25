"""
Datenmodelle für das Spec-Tool.
Alle Modelle sind Pydantic v2 und bilden die interne Repräsentation
der geparsten Spezifikationsdokumente.
"""
from __future__ import annotations

from enum import Enum
from pathlib import Path
from typing import Any, Optional

from pydantic import BaseModel, Field


# ─────────────────────────────────────────────────────────────
# Enums
# ─────────────────────────────────────────────────────────────

class DocType(str, Enum):
    CHARTER = "charter"
    CONTRACTS = "contracts"
    SPEC = "spec"
    TEST_STRATEGY = "test-strategy"
    ROADMAP = "roadmap"
    VIEW = "view"
    PATCH = "patch"
    FORMAT_DEFINITION = "format-definition"


class Layer(str, Enum):
    FOUNDATION = "foundation"
    SPECS = "specs"
    OPS = "ops"
    VIEWS = "views"
    PATCHES = "patches"
    ARCHIVE = "archive"


class SectionType(str, Enum):
    META = "meta"
    PROSE = "prose"
    CHANGE_REQUEST = "change-request"
    CONTRACT = "contract"
    ENUM = "enum"
    STATE_MACHINE = "state-machine"
    DATAFLOW = "dataflow"
    ROLE_DEFINITION = "role-definition"
    TEST_SUITE = "test-suite"
    TEST_CASE = "test-case"
    SAFETY_RULE = "safety-rule"
    IMPLEMENTATION_PHASE = "implementation-phase"
    ACCEPTANCE = "acceptance"
    CONFIG = "config"


class MarkerType(str, Enum):
    SECTION = "section"
    TABLE = "table"
    REF = "ref"
    ROLE = "role"
    ROLE_REF = "role-ref"
    CONTRACT = "contract"
    STATE_MACHINE = "state_machine"
    DATAFLOW = "dataflow"
    DATAFLOW_STEP = "dataflow-step"
    SAFETY_RULE = "safety-rule"
    TEST = "test"


class ReferenceType(str, Enum):
    SECURITY_RULE = "security-rule"
    CONTRACT = "contract"
    SPEC = "spec"
    ENUM = "enum"
    ROLE = "role"
    DATAFLOW = "dataflow"
    TEST = "test"
    CONFIG = "config"


class ConflictRule(str, Enum):
    CHARTER = "CHARTER"
    CONTRACTS = "CONTRACTS"
    SPECS = "SPECS"
    VALIDATION = "VALIDATION"
    THIS_DOC = "THIS_DOC"


# ─────────────────────────────────────────────────────────────
# Frontmatter
# ─────────────────────────────────────────────────────────────

class Frontmatter(BaseModel):
    """YAML-Frontmatter einer Spezifikationsdatei."""
    doc_id: str
    doc_type: DocType
    version: str
    status: str
    schema_version: str = "spec-format-1.0"
    layer: Layer
    builds_on: list[str] = Field(default_factory=list)
    conflict_rule: list[ConflictRule] = Field(default_factory=list)
    roles_defined: list[str] = Field(default_factory=list)
    roles_referenced: list[str] = Field(default_factory=list)
    dataflows_defined: list[str] = Field(default_factory=list)
    last_modified: Optional[str] = None


# ─────────────────────────────────────────────────────────────
# Marker
# ─────────────────────────────────────────────────────────────

class Marker(BaseModel):
    """Ein HTML-Kommentar-Marker wie <!-- @section ... -->"""
    marker_type: MarkerType
    attributes: dict[str, Any] = Field(default_factory=dict)
    line_number: int = 0
    raw: str = ""


# ─────────────────────────────────────────────────────────────
# Querverweis
# ─────────────────────────────────────────────────────────────

class Reference(BaseModel):
    """Ein Querverweis zwischen zwei Dokumenten oder Abschnitten."""
    source_doc: str
    source_section: Optional[str] = None
    target_doc: str
    target_section: Optional[str] = None
    reference_type: ReferenceType
    raw_text: str = ""
    line_number: int = 0

    @property
    def is_cross_document(self) -> bool:
        return self.source_doc != self.target_doc

    @property
    def is_cross_layer(self) -> bool:
        source_layer = self.source_doc.split("/")[0] if "/" in self.source_doc else ""
        target_layer = self.target_doc.split("/")[0] if "/" in self.target_doc else ""
        return source_layer != target_layer


# ─────────────────────────────────────────────────────────────
# Tabelle
# ─────────────────────────────────────────────────────────────

class ParsedTable(BaseModel):
    """Eine geparste Markdown-Tabelle."""
    schema_name: Optional[str] = None
    headers: list[str] = Field(default_factory=list)
    rows: list[list[str]] = Field(default_factory=list)
    line_number: int = 0

    @property
    def row_count(self) -> int:
        return len(self.rows)


# ─────────────────────────────────────────────────────────────
# Section
# ─────────────────────────────────────────────────────────────

class Section(BaseModel):
    """Ein Abschnitt eines Spezifikationsdokuments."""
    section_id: str
    title: str
    section_type: SectionType = SectionType.PROSE
    level: int = 1
    content: str = ""
    markers: list[Marker] = Field(default_factory=list)
    tables: list[ParsedTable] = Field(default_factory=list)
    references: list[Reference] = Field(default_factory=list)
    children: list[Section] = Field(default_factory=list)
    line_number: int = 0

    # Rollen-spezifisch
    role_id: Optional[str] = None
    role_layer: Optional[int] = None
    role_llm: Optional[bool] = None

    # Vertrags-spezifisch
    contract_name: Optional[str] = None
    contract_type: Optional[str] = None

    # Datenfluss-spezifisch
    dataflow_id: Optional[str] = None
    dataflow_trigger: Optional[str] = None
    dataflow_steps: list[dict[str, Any]] = Field(default_factory=list)

    # Sicherheitsregel-spezifisch
    safety_rule_id: Optional[str] = None

    @property
    def full_id(self) -> str:
        return self.section_id


# ─────────────────────────────────────────────────────────────
# Dokument
# ─────────────────────────────────────────────────────────────

class SpecDocument(BaseModel):
    """Ein vollständig geparstes Spezifikationsdokument."""
    file_path: Path
    frontmatter: Optional[Frontmatter] = None
    sections: list[Section] = Field(default_factory=list)
    references: list[Reference] = Field(default_factory=list)
    markers: list[Marker] = Field(default_factory=list)
    tables: list[ParsedTable] = Field(default_factory=list)
    raw_content: str = ""
    parse_errors: list[str] = Field(default_factory=list)

    @property
    def doc_id(self) -> str:
        if self.frontmatter:
            return self.frontmatter.doc_id
        return str(self.file_path)

    @property
    def version(self) -> str:
        if self.frontmatter:
            return self.frontmatter.version
        return "unknown"

    @property
    def layer(self) -> Optional[Layer]:
        if self.frontmatter:
            return self.frontmatter.layer
        return None

    @property
    def roles_defined(self) -> list[str]:
        if self.frontmatter:
            return self.frontmatter.roles_defined
        return []

    @property
    def section_count(self) -> int:
        return len(self.sections)

    @property
    def reference_count(self) -> int:
        return len(self.references)

    def get_section(self, section_id: str) -> Optional[Section]:
        """Sucht einen Abschnitt nach ID (rekursiv)."""
        for section in self.sections:
            if section.section_id == section_id:
                return section
            found = _find_section_recursive(section, section_id)
            if found:
                return found
        return None

    def get_sections_by_type(self, section_type: SectionType) -> list[Section]:
        """Gibt alle Abschnitte eines bestimmten Typs zurück."""
        result = []
        for section in self.sections:
            _collect_sections_by_type(section, section_type, result)
        return result

    def get_roles(self) -> list[Section]:
        """Gibt alle Rollen-Abschnitte zurück."""
        return self.get_sections_by_type(SectionType.ROLE_DEFINITION)

    def get_contracts(self) -> list[Section]:
        """Gibt alle Vertrags-Abschnitte zurück."""
        return self.get_sections_by_type(SectionType.CONTRACT)

    def get_dataflows(self) -> list[Section]:
        """Gibt alle Datenfluss-Abschnitte zurück."""
        return self.get_sections_by_type(SectionType.DATAFLOW)


def _find_section_recursive(section: Section, section_id: str) -> Optional[Section]:
    for child in section.children:
        if child.section_id == section_id:
            return child
        found = _find_section_recursive(child, section_id)
        if found:
            return found
    return None


def _collect_sections_by_type(section: Section, section_type: SectionType, result: list[Section]):
    if section.section_type == section_type:
        result.append(section)
    for child in section.children:
        _collect_sections_by_type(child, section_type, result)