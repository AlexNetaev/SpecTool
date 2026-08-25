"""Tests für den Frontmatter-Parser."""
import pytest
from spec_tool.parser.frontmatter import parse_frontmatter
from spec_tool.models import DocType, Layer


class TestParseFrontmatter:

    def test_valid_frontmatter(self):
        content = """---
doc_id: foundation/CHARTER.md
doc_type: charter
version: 1.0.0
status: BINDEND
schema_version: spec-format-1.0
layer: foundation
builds_on: []
conflict_rule: []
last_modified: 2026-08-21
---

# Titel
"""
        fm, rest = parse_frontmatter(content)
        assert fm is not None
        assert fm.doc_id == "foundation/CHARTER.md"
        assert fm.doc_type == DocType.CHARTER
        assert fm.version == "1.0.0"
        assert fm.status == "BINDEND"
        assert fm.layer == Layer.FOUNDATION
        assert "# Titel" in rest

    def test_missing_frontmatter(self):
        content = "# Titel\n\nInhalt"
        fm, rest = parse_frontmatter(content)
        assert fm is None
        assert rest == content

    def test_invalid_yaml(self):
        content = """---
doc_id: [invalid yaml
---

# Titel
"""
        fm, rest = parse_frontmatter(content)
        assert fm is None

    def test_frontmatter_with_builds_on(self):
        content = """---
doc_id: specs/QUESTOR.md
doc_type: spec
version: 1.1.0
status: BINDEND
layer: specs
builds_on:
  - foundation/CHARTER.md@1.0.0
  - foundation/CONTRACTS.md@1.2.1
---
"""
        fm, _ = parse_frontmatter(content)
        assert fm is not None
        assert len(fm.builds_on) == 2
        assert fm.builds_on[0] == "foundation/CHARTER.md@1.0.0"

    def test_unknown_doc_type_defaults_to_spec(self):
        content = """---
doc_id: test.md
doc_type: unknown_type
version: 1.0.0
status: BINDEND
layer: specs
---
"""
        fm, _ = parse_frontmatter(content)
        assert fm is not None
        assert fm.doc_type == DocType.SPEC

    def test_unknown_layer_defaults_to_specs(self):
        content = """---
doc_id: test.md
doc_type: spec
version: 1.0.0
status: BINDEND
layer: unknown_layer
---
"""
        fm, _ = parse_frontmatter(content)
        assert fm is not None
        assert fm.layer == Layer.SPECS