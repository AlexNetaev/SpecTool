"""
Debug-Skript: Warum findet der Parser keine Abschnitte in CONTRACTS.md?
"""
import re
from pathlib import Path

# ── Pfad zur Datei ──
CONTRACTS_PATH = Path("data/foundation/CONTRACTS.md")

# ── Regex-Patterns (identisch zum Parser) ──
HEADING_PATTERN = re.compile(r"^(#{1,6})\s+(.+)$", re.MULTILINE)
SECTION_NUM_PATTERN = re.compile(r"§([\d]+(?:\.[\d]+)*)")
FRONTMATTER_PATTERN = re.compile(r"^\ufeff?---\s*\r?\n(.*?)\r?\n---\s*\r?\n", re.DOTALL)
SECTION_MARKER_PATTERN = re.compile(r"<!--\s*@section\s+(.*?)-->", re.DOTALL)

def main():
    print("=" * 70)
    print(f"DEBUG: {CONTRACTS_PATH}")
    print("=" * 70)

    if not CONTRACTS_PATH.exists():
        print("❌ DATEI NICHT GEFUNDEN!")
        return

    content = CONTRACTS_PATH.read_text(encoding="utf-8")
    lines = content.split("\n")

    print(f"\n📊 Datei-Statistiken:")
    print(f"  Gesamtzeilen: {len(lines)}")
    print(f"  Gesamtzeichen: {len(content)}")

    # ── 1. Frontmatter prüfen ──
    print(f"\n{'='*70}")
    print("1. FRONTMATTER-PRÜFUNG")
    print(f"{'='*70}")

    fm_match = FRONTMATTER_PATTERN.match(content)
    if fm_match:
        print("  ✅ Frontmatter GEFUNDEN")
        print(f"  Frontmatter-Inhalt (erste 5 Zeilen):")
        fm_lines = fm_match.group(1).split("\n")[:5]
        for line in fm_lines:
            print(f"    {line}")
        body = content[fm_match.end():]
    else:
        print("  ❌ Frontmatter NICHT gefunden!")
        print(f"  Erste 3 Zeilen der Datei:")
        for i, line in enumerate(lines[:3]):
            print(f"    Zeile {i+1}: '{line}'")
        body = content

    # ── 2. Markdown-Überschriften suchen ──
    print(f"\n{'='*70}")
    print("2. MARKDOWN-ÜBERSCHRIFTEN (## ... ####)")
    print(f"{'='*70}")

    headings = HEADING_PATTERN.findall(body)
    print(f"  Gefundene Überschriften: {len(headings)}")

    if headings:
        print(f"  Erste 10 Überschriften:")
        for i, (level, title) in enumerate(headings[:10]):
            print(f"    {level} {title}")
    else:
        print("  ❌ KEINE Markdown-Überschriften gefunden!")
        print("  → Der Parser findet KEINE Abschnitte!")
        print()
        print("  Mögliche Ursachen:")
        print("    a) Die Datei verwendet KEINE '##'-Überschriften")
        print("    b) Die Abschnitte sind als reine Textzeilen formatiert")
        print("    c) Die Datei ist die ALTE Version ohne Migration")

    # ── 3. @section-Marker suchen ──
    print(f"\n{'='*70}")
    print("3. @section-MARKER")
    print(f"{'='*70}")

    section_markers = SECTION_MARKER_PATTERN.findall(body)
    print(f"  Gefundene @section-Marker: {len(section_markers)}")

    if section_markers:
        print(f"  Erste 5 Marker:")
        for i, marker in enumerate(section_markers[:5]):
            print(f"    <!-- @section {marker.strip()[:80]}... -->")
    else:
        print("  ❌ KEINE @section-Marker gefunden!")

    # ── 4. §-Abschnittsnummern suchen ──
    print(f"\n{'='*70}")
    print("4. §-ABSCHNITTSNUMMERN")
    print(f"{'='*70}")

    section_nums = SECTION_NUM_PATTERN.findall(body)
    print(f"  Gefundene §-Nummern: {len(section_nums)}")

    if section_nums:
        print(f"  Erste 10 Nummern: {section_nums[:10]}")
    else:
        print("  ❌ KEINE §-Nummern gefunden!")

    # ── 5. Erste 30 Zeilen der Datei (nach Frontmatter) ──
    print(f"\n{'='*70}")
    print("5. ERSTE 30 ZEILEN NACH FRONTMATTER")
    print(f"{'='*70}")

    body_lines = body.split("\n")
    for i, line in enumerate(body_lines[:30], start=1):
        marker = ""
        if HEADING_PATTERN.match(line):
            marker = " ← ÜBERSCHRIFT"
        elif line.strip().startswith("<!--"):
            marker = " ← KOMMENTAR"
        elif line.strip().startswith("§"):
            marker = " ← §-TEXTZEILE (keine ##-Überschrift!)"
        elif line.strip() and not line.strip().startswith("|"):
            marker = " ← TEXTZEILE"
        print(f"  {i:3d}: {line[:90]}{marker}")

    # ── 6. Diagnose ──
    print(f"\n{'='*70}")
    print("6. DIAGNOSE")
    print(f"{'='*70}")

    if not headings and section_nums:
        print("  ⚠️  PROBLEM ERKANNT:")
        print("  Die Datei enthält §-Abschnittsnummern als TEXTZEILEN,")
        print("  aber KEINE Markdown-Überschriften (## ...).")
        print()
        print("  Der Parser sucht nach: ^(#{1,6})\\s+(.+)$")
        print("  Die Datei enthält aber Zeilen wie: '§1 Paket-Verträge'")
        print("  statt: '## §1 Paket-Verträge'")
        print()
        print("  LÖSUNG:")
        print("  Die Datei im data/-Verzeichnis muss die MIGRIERTE Version")
        print("  mit '##'-Überschriften sein, nicht die alte Version.")
        print()
        print("  Beispiel:")
        print("    FALSCH:  §1 Paket-Verträge")
        print("    RICHTIG: ## §1 Paket-Verträge")
    elif not headings and not section_nums:
        print("  ⚠️  PROBLEM: Weder Überschriften noch §-Nummern gefunden.")
        print("  Die Datei ist möglicherweise leer oder korrupt.")
    elif headings:
        print("  ✅ Überschriften vorhanden. Problem liegt woanders.")


if __name__ == "__main__":
    main()