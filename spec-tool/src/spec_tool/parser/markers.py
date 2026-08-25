"""
Parser für HTML-Kommentar-Marker in Spezifikationsdateien.
Erkennt Marker wie:
  <!-- @section id="3.2" title="Kartograph" type="role-definition" role="kartograph" -->
  <!-- @table schema="test_cases" suite="ATLAS-CTR" -->
  <!-- @ref target="CHARTER §SR-04" type="security-rule" -->
  <!-- @role id="kartograph" layer="4" llm="false" -->
  <!-- @dataflow id="twin_drift" trigger="TWIN_DIVERGENCE" -->
  <!-- @dataflow-step order="1" -->
  <!-- @safety-rule id="SR-04" category="grundregel" -->
"""
from __future__ import annotations

import re
from typing import Any

from spec_tool.models import Marker, MarkerType


# Regex für HTML-Kommentar-Marker
MARKER_PATTERN = re.compile(
    r"<!--\s*@([\w-]+)\s+(.*?)-->",
    re.DOTALL,
)

# Regex für Attribut-Paare: key="value" oder key='value'
ATTR_PATTERN = re.compile(
    r"""([\w-]+)\s*=\s*(?:"([^"]*)"|'([^']*)')""",
)

# Mapping von Marker-Namen zu MarkerType
MARKER_TYPE_MAP: dict[str, MarkerType] = {
    "section": MarkerType.SECTION,
    "table": MarkerType.TABLE,
    "ref": MarkerType.REF,
    "role": MarkerType.ROLE,
    "role-ref": MarkerType.ROLE_REF,
    "contract": MarkerType.CONTRACT,
    "state_machine": MarkerType.STATE_MACHINE,
    "state-machine": MarkerType.STATE_MACHINE,
    "dataflow": MarkerType.DATAFLOW,
    "dataflow-step": MarkerType.DATAFLOW_STEP,
    "safety-rule": MarkerType.SAFETY_RULE,
    "test": MarkerType.TEST,
}


def parse_markers(content: str) -> list[Marker]:
    """
    Extrahiert alle HTML-Kommentar-Marker aus dem Inhalt.

    Returns:
        Liste von Marker-Objekten, sortiert nach Zeilennummer.
    """
    markers = []
    lines = content.split("\n")

    for line_num, line in enumerate(lines, start=1):
        for match in MARKER_PATTERN.finditer(line):
            marker_name = match.group(1)
            attrs_str = match.group(2)

            marker_type = MARKER_TYPE_MAP.get(marker_name)
            if marker_type is None:
                continue

            attributes = _parse_attributes(attrs_str)

            markers.append(Marker(
                marker_type=marker_type,
                attributes=attributes,
                line_number=line_num,
                raw=match.group(0).strip(),
            ))

    return markers


def parse_markers_multiline(content: str) -> list[Marker]:
    """
    Extrahiert Marker auch über mehrere Zeilen (für mehrzeilige Kommentare).
    """
    markers = []

    for match in MARKER_PATTERN.finditer(content):
        marker_name = match.group(1)
        attrs_str = match.group(2)

        marker_type = MARKER_TYPE_MAP.get(marker_name)
        if marker_type is None:
            continue

        attributes = _parse_attributes(attrs_str)

        # Zeilennummer berechnen
        line_number = content[:match.start()].count("\n") + 1

        markers.append(Marker(
            marker_type=marker_type,
            attributes=attributes,
            line_number=line_number,
            raw=match.group(0).strip(),
        ))

    return markers


def _parse_attributes(attrs_str: str) -> dict[str, Any]:
    """Parst Attribut-Paare aus einem Marker-String."""
    attributes: dict[str, Any] = {}

    for match in ATTR_PATTERN.finditer(attrs_str):
        key = match.group(1)
        value = match.group(2) if match.group(2) is not None else match.group(3)

        # Typ-Konvertierung
        if value.lower() == "true":
            attributes[key] = True
        elif value.lower() == "false":
            attributes[key] = False
        elif value.isdigit():
            attributes[key] = int(value)
        else:
            attributes[key] = value

    return attributes