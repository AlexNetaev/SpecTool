"""Tests für den Marker-Parser."""
import pytest
from spec_tool.parser.markers import parse_markers_multiline
from spec_tool.models import MarkerType


class TestParseMarkers:

    def test_section_marker(self):
        """M-01: @section-Marker wird erkannt."""
        content = '<!-- @section id="3.2" title="Kartograph" type="role-definition" -->'
        markers = parse_markers_multiline(content)
        assert len(markers) == 1
        assert markers[0].marker_type == MarkerType.SECTION
        assert markers[0].attributes["id"] == "3.2"
        assert markers[0].attributes["title"] == "Kartograph"

    def test_role_marker(self):
        """M-02: @role-Marker wird erkannt."""
        content = '<!-- @role id="kartograph" layer="4" llm="false" -->'
        markers = parse_markers_multiline(content)
        assert len(markers) == 1
        assert markers[0].marker_type == MarkerType.ROLE
        assert markers[0].attributes["id"] == "kartograph"
        assert markers[0].attributes["layer"] == 4
        assert markers[0].attributes["llm"] is False

    def test_ref_marker(self):
        """M-03: @ref-Marker wird erkannt."""
        content = '<!-- @ref target="CHARTER §SR-04" type="security-rule" -->'
        markers = parse_markers_multiline(content)
        assert len(markers) == 1
        assert markers[0].marker_type == MarkerType.REF
        assert markers[0].attributes["target"] == "CHARTER §SR-04"

    def test_table_marker(self):
        """M-04: @table-Marker wird erkannt."""
        content = '<!-- @table schema="role_permissions" role="kartograph" -->'
        markers = parse_markers_multiline(content)
        assert len(markers) == 1
        assert markers[0].marker_type == MarkerType.TABLE
        assert markers[0].attributes["schema"] == "role_permissions"

    def test_dataflow_marker(self):
        """M-05: @dataflow-Marker wird erkannt."""
        content = '<!-- @dataflow id="twin_drift" trigger="TWIN_DIVERGENCE" -->'
        markers = parse_markers_multiline(content)
        assert len(markers) == 1
        assert markers[0].marker_type == MarkerType.DATAFLOW
        assert markers[0].attributes["trigger"] == "TWIN_DIVERGENCE"

    def test_safety_rule_marker(self):
        """M-06: @safety-rule-Marker wird erkannt."""
        content = '<!-- @safety-rule id="SR-04" category="grundregel" -->'
        markers = parse_markers_multiline(content)
        assert len(markers) == 1
        assert markers[0].marker_type == MarkerType.SAFETY_RULE
        assert markers[0].attributes["id"] == "SR-04"

    def test_unknown_marker_ignored(self):
        """M-07: Unbekannte Marker werden ignoriert."""
        content = '<!-- @unknown_marker foo="bar" -->'
        markers = parse_markers_multiline(content)
        assert len(markers) == 0

    def test_multiple_markers(self):
        """M-08: Mehrere Marker in einer Datei werden alle erkannt."""
        content = """
<!-- @section id="1" title="Test" type="prose" -->
<!-- @role id="test_role" layer="1" -->
<!-- @ref target="CHARTER §SR-01" type="security-rule" -->
"""
        markers = parse_markers_multiline(content)
        assert len(markers) == 3

    def test_line_numbers_correct(self):
        """M-09: Zeilennummern sind korrekt."""
        content = "Zeile 1\n<!-- @section id=\"1\" title=\"Test\" type=\"prose\" -->\nZeile 3"
        markers = parse_markers_multiline(content)
        assert len(markers) == 1
        assert markers[0].line_number == 2

    def test_contract_marker(self):
        """M-10: @contract-Marker wird erkannt."""
        content = '<!-- @contract name="DigitalTwinModel" type="pydantic" section="6.10.19" -->'
        markers = parse_markers_multiline(content)
        assert len(markers) == 1
        assert markers[0].marker_type == MarkerType.CONTRACT
        assert markers[0].attributes["name"] == "DigitalTwinModel"

    def test_state_machine_marker(self):
        """M-11: @state-machine-Marker wird erkannt."""
        content = '<!-- @state-machine id="questor_state" states="11" -->'
        markers = parse_markers_multiline(content)
        assert len(markers) == 1
        assert markers[0].marker_type == MarkerType.STATE_MACHINE