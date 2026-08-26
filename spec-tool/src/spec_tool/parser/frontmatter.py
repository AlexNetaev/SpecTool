"""
Parser für YAML-Frontmatter in Spezifikationsdateien.
"""
from __future__ import annotations

import datetime
import re
from typing import Optional

import yaml

from spec_tool.models import Frontmatter, DocType, Layer, ConflictRule


# ── FIX: Regex robuster gemacht ──
# Erlaubt optionales BOM, \r\n und \n Zeilenenden
FRONTMATTER_PATTERN = re.compile(
    r"^\ufeff?---\s*\r?\n(.*?)\r?\n---\s*\r?\n",
    re.DOTALL,
)


def parse_frontmatter(content: str) -> tuple[Optional[Frontmatter], str]:
    """
    Parst den YAML-Frontmatter aus dem Inhalt einer Spezifikationsdatei.

    Returns:
        Tuple aus (Frontmatter | None, restlicher Inhalt ohne Frontmatter)
    """
    match = FRONTMATTER_PATTERN.match(content)
    if not match:
        return None, content

    yaml_str = match.group(1)
    rest = content[match.end():]

    try:
        data = yaml.safe_load(yaml_str)
    except yaml.YAMLError:
        return None, rest

    if not isinstance(data, dict):
        return None, rest

    # ── FIX: datetime.date → str konvertieren ──
    # PyYAML parst "2026-08-21" als datetime.date-Objekt.
    # Pydantic erwartet Optional[str].
    if "last_modified" in data and isinstance(data["last_modified"], datetime.date):
        data["last_modified"] = data["last_modified"].isoformat()

    # ── FIX: builds_on und conflict_rule als Listen sicherstellen ──
    if data.get("builds_on") is None:
        data["builds_on"] = []
    if data.get("conflict_rule") is None:
        data["conflict_rule"] = []
    if data.get("roles_defined") is None:
        data["roles_defined"] = []
    if data.get("roles_referenced") is None:
        data["roles_referenced"] = []
    if data.get("dataflows_defined") is None:
        data["dataflows_defined"] = []

    try:
        frontmatter = Frontmatter(
            doc_id=str(data.get("doc_id", "")),
            doc_type=_parse_doc_type(str(data.get("doc_type", "spec"))),
            version=str(data.get("version", "0.0.0")),
            status=str(data.get("status", "BINDEND")),
            schema_version=str(data.get("schema_version", "spec-format-1.0")),
            layer=_parse_layer(str(data.get("layer", "specs"))),
            builds_on=[str(x) for x in data.get("builds_on", [])],
            conflict_rule=_parse_conflict_rules(data.get("conflict_rule", [])),
            roles_defined=[str(x) for x in data.get("roles_defined", [])],
            roles_referenced=[str(x) for x in data.get("roles_referenced", [])],
            dataflows_defined=[str(x) for x in data.get("dataflows_defined", [])],
            last_modified=str(data.get("last_modified")) if data.get("last_modified") else None,
        )
        return frontmatter, rest
    except Exception:
        return None, rest


def _parse_doc_type(value: str) -> DocType:
    try:
        return DocType(value)
    except ValueError:
        return DocType.SPEC


def _parse_layer(value: str) -> Layer:
    try:
        return Layer(value)
    except ValueError:
        return Layer.SPECS


def _parse_conflict_rules(values: list) -> list[ConflictRule]:
    result = []
    for v in values:
        try:
            result.append(ConflictRule(str(v)))
        except ValueError:
            pass
    return result