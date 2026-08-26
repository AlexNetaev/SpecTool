"""
Parser für SPEC_FORMAT Marker (HTML-Kommentare).
Erkennt und parst alle Marker-Typen aus Markdown-Dateien.
"""
from __future__ import annotations

import re
from typing import Any

from spec_tool.models import Marker, MarkerType


# ─────────────────────────────────────────────────────────────
# Regex-Patterns für verschiedene Marker-Typen
# ─────────────────────────────────────────────────────────────

# Generischer Pattern für alle Marker
MARKER_PATTERN = re.compile(
    r"<!--\s*@([\w-]+)(.*?)-->",
    re.DOTALL
)

# Spezifische Patterns für komplexere Marker
ROLE_MARKER_PATTERN = re.compile(
    r"<!--\s*@role\s+([^>]*?)\s*-->",
    re.DOTALL
)

DATAFLOW_MARKER_PATTERN = re.compile(
    r"<!--\s*@dataflow\s+([^>]*?)\s*-->",
    re.DOTALL
)

DATAFLOW_STEP_PATTERN = re.compile(
    r"<!--\s*@dataflow-step\s+([^>]*?)\s*-->",
    re.DOTALL
)

# Pattern für Attribute (key="value" oder key='value')
ATTRIBUTE_PATTERN = re.compile(
    r'(\w+)=["\']([^"\']*?)["\']'
)


def parse_markers(content: str) -> list[Marker]:
    """
    Parst alle Marker aus dem Inhalt.

    Args:
        content: Der Markdown-Inhalt mit Markern

    Returns:
        Liste von Marker-Objekten
    """
    markers: list[Marker] = []

    # Windows-Zeilenenden normalisieren
    content = content.replace("\r\n", "\n").replace("\r", "\n")

    for match in MARKER_PATTERN.finditer(content):
        marker_type_str = match.group(1)
        attrs_str = match.group(2).strip()

        # Zeilennummer berechnen
        line_num = content[:match.start()].count('\n') + 1

        # Marker-Typ bestimmen
        try:
            marker_type = MarkerType(marker_type_str)
        except ValueError:
            # Unbekannter Marker-Typ wird ignoriert
            continue

        # Attribute parsen
        attributes = _parse_attributes(attrs_str)

        markers.append(
            Marker(
                marker_type=marker_type,
                raw=match.group(0),
                line_number=line_num,
                attributes=attributes,
            )
        )

    return markers


def parse_markers_multiline(content: str) -> list[Marker]:
    """
    Parst Marker aus mehrzeiligem Inhalt.
    Identisch zu parse_markers, aber mit explizitem Namen für Klarheit.

    Args:
        content: Der Markdown-Inhalt mit Markern

    Returns:
        Liste von Marker-Objekten
    """
    markers: list[Marker] = []

    # Windows-Zeilenenden normalisieren
    content = content.replace("\r\n", "\n").replace("\r", "\n")

    for match in MARKER_PATTERN.finditer(content):
        marker_type_str = match.group(1)
        attrs_str = match.group(2).strip()

        # Zeilennummer berechnen
        line_num = content[:match.start()].count('\n') + 1

        # Marker-Typ bestimmen
        try:
            marker_type = MarkerType(marker_type_str)
        except ValueError:
            # Unbekannter Marker-Typ wird ignoriert
            continue

        # Attribute parsen
        attributes = _parse_attributes(attrs_str)

        # Spezielle Behandlung für bestimmte Marker-Typen
        if marker_type == MarkerType.ROLE:
            # llm-Attribut kann bool oder str sein
            llm_val = attributes.get("llm")
            if llm_val is not None:
                if isinstance(llm_val, str):
                    # Konvertiere "true"/"false" zu bool
                    attributes["llm"] = llm_val.lower() == "true"
                # Wenn es bereits bool ist, bleibt es so

        markers.append(
            Marker(
                marker_type=marker_type,
                raw=match.group(0),
                line_number=line_num,
                attributes=attributes,
            )
        )

    return markers


def _parse_attributes(attrs_str: str) -> dict[str, Any]:
    """
    Parst Attribute aus einem Marker-String.

    Args:
        attrs_str: Der Attribut-Teil des Markers (z.B. 'id="0" title="Test"')

    Returns:
        Dictionary mit Attribut-Namen als Keys und Werten
    """
    attributes: dict[str, Any] = {}

    for match in ATTRIBUTE_PATTERN.finditer(attrs_str):
        key = match.group(1)
        value = match.group(2)

        # Spezielle Behandlung für bestimmte Attribute
        if key == "llm":
            # llm kann bool sein
            attributes[key] = value.lower() == "true"
        elif key in ["layer", "order", "line"]:
            # Numerische Attribute
            try:
                attributes[key] = int(value)
            except ValueError:
                attributes[key] = value
        else:
            attributes[key] = value

    return attributes


def get_markers_by_type(markers: list[Marker], marker_type: MarkerType) -> list[Marker]:
    """
    Filtert Marker nach Typ.

    Args:
        markers: Liste von Markern
        marker_type: Der gesuchte Marker-Typ

    Returns:
        Liste von Markern des angegebenen Typs
    """
    return [m for m in markers if m.marker_type == marker_type]


def find_marker_near_line(
    markers: list[Marker],
    line_num: int,
    marker_type: MarkerType,
    max_distance: int = 5,
) -> Marker | None:
    """
    Findet einen Marker in der Nähe einer bestimmten Zeile.

    Args:
        markers: Liste von Markern
        line_num: Die Ziel-Zeilennummer
        marker_type: Der gesuchte Marker-Typ
        max_distance: Maximale Entfernung in Zeilen

    Returns:
        Der nächste Marker oder None
    """
    candidates = [
        m for m in markers
        if m.marker_type == marker_type
        and abs(m.line_number - line_num) <= max_distance
    ]

    if not candidates:
        return None

    # Sortiere nach Entfernung und gib den nächsten zurück
    candidates.sort(key=lambda m: abs(m.line_number - line_num))
    return candidates[0]