"""
Parser für YAML-Frontmatter in Spezifikationsdateien.
"""
from __future__ import annotations

import re
from typing import Optional

import yaml

from spec_tool.models import Frontmatter, DocType, Layer, ConflictRule


FRONTMATTER_PATTERN = re.compile(
    r"^---\s*\n(.*?)\n---\s*\n",
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
    except yaml.YAMLError as e:
        return None, rest

    if not isinstance(data, dict):
        return None, rest

    try:
        frontmatter = Frontmatter(
            doc_id=data.get("doc_id", ""),
            doc_type=_parse_doc_type(data.get("doc_type", "spec")),
            version=data.get("version", "0.0.0"),
            status=data.get("status", "BINDEND"),
            schema_version=data.get("schema_version", "spec-format-1.0"),
            layer=_parse_layer(data.get("layer", "specs")),
            builds_on=data.get("builds_on", []),
            conflict_rule=_parse_conflict_rules(data.get("conflict_rule", [])),
            roles_defined=data.get("roles_defined", []),
            roles_referenced=data.get("roles_referenced", []),
            dataflows_defined=data.get("dataflows_defined", []),
            last_modified=data.get("last_modified"),
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
            result.append(ConflictRule(v))
        except ValueError:
            pass
    return result