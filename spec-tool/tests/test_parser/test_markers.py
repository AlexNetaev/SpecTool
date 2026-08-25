"""Tests für den Marker-Parser."""
import pytest
from spec_tool.parser.markers import parse_markers_multiline, _parse_attributes
from spec_tool.models import MarkerType


class TestParseMarkers:

    def test_section_marker(self):
        content = '<!-- @section id="3.2" title="Kartograph" type="role-definition" -->'
        markers = parse_markers_multiline(content)
        assert len(markers) == 1
        assert markers[0].marker_type == MarkerType.SECTION
        assert markers[0].attributes["id"] == "3.2"
        assert markers[0].attributes["title"] == "Kartograph"
        assert markers[0].attributes["type"] == "role-definition"

    def test_role_marker(self):
        content = '<!-- @role id="kartograph" layer="4" llm="false" -->'
        markers = parse_markers_multiline(content)
        assert len(markers) == 1
        assert markers[0].marker_type == MarkerType.ROLE
        assert markers[0].attributes["id"] == "kartograph"
        assert markers[0].attributes["layer"] == 4
        assert markers[0].attributes["llm"] is False

    def test_ref_marker(self):
        content = '<!-- @ref target="CHARTER §SR-04" type="security-rule" -->'
        markers = parse_markers_multiline(content)
        assert len(markers) == 1
        assert markers[0].marker_type == MarkerType.REF
        assert markers[0].attributes["target"] == "CHARTER §SR-04"

    def test_table_marker(self):
        content = '<!-- @table schema="role_permissions" role="kartograph" -->'
        markers = parse_markers_multiline(content)
        assert len(markers) == 1
        assert markers[0].marker_type == MarkerType.TABLE
        assert markers[0].attributes["schema"] == "role_permissions"

    def test_dataflow_marker(self):
        content = '<!-- @dataflow id="twin_drift" trigger="TWIN_DIVERGENCE" -->'
        markers = parse_markers_multiline(content)
        assert len(markers) == 1
        assert markers[0].marker_type == MarkerType.DATAFLOW
        assert markers[0].attributes["id"] == "twin_drift"
        assert markers[0].attributes["trigger"] == "TWIN_DIVERGENCE"

    def test_unknown_marker_ignored(self):
        content = '<!-- @unknown_marker foo="bar" -->'
        markers = parse_markers_multiline(content)
        assert len(markers) == 0

    def test_multiple_markers(self):
        content = """
<!-- @section id="1" title="Test" type="prose" -->
<!-- @role id="test_role" layer="1" -->
<!-- @ref target="CHARTER §SR-01" type="security-rule" -->
"""
        markers = parse_markers_multiline(content)
        assert len(markers) == 3

    def test_line_numbers(self):
        content = "Zeile 1\n<!-- @section id=\"1\" title=\"Test\" type=\"prose\" -->\nZeile 3"
        markers = parse_markers_multiline(content)
        assert len(markers) == 1
        assert markers[0].line_number == 2


class TestParseAttributes:

    def test_string_attribute(self):
        attrs = _parse_attributes('id="test" name="wert"')
        assert attrs["id"] == "test"
        assert attrs["name"] == "wert"

    def test_integer_attribute(self):
        attrs = _parse_attributes('layer="4" count="10"')
        assert attrs["layer"] == 4
        assert attrs["count"] == 10

    def test_boolean_attribute(self):
        attrs = _parse_attributes('llm="true" active="false"')
        assert attrs["llm"] is True
        assert attrs["active"] is False

    def test_single_quotes(self):
        attrs = _parse_attributes("id='test' name='wert'")
        assert attrs["id"] == "test"
        assert attrs["name"] == "wert"