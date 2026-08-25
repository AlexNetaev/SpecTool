"""
CLI-Einstiegspunkt für das Spec-Tool.

Verwendung:
    spec-tool parse <datei>          # Eine Datei parsen
    spec-tool parse-all <verzeichnis> # Alle Dateien in einem Verzeichnis parsen
    spec-tool validate <verzeichnis>  # Konsistenz prüfen
    spec-tool impact <datei> [abschnitt]  # Impact-Analyse
    spec-tool stats <verzeichnis>     # Statistiken anzeigen
    spec-tool graph <verzeichnis>     # Referenzgraph anzeigen
"""
from __future__ import annotations

from pathlib import Path

import click
from rich.console import Console
from rich.table import Table
from rich.tree import Tree

from spec_tool.parser.md_parser import MarkdownParser
from spec_tool.graph.reference_graph import ReferenceGraph

console = Console()


@click.group()
def main():
    """Spec-Tool: Parser, Validator und View-Generator für Spezifikationsdokumente."""
    pass


@main.command()
@click.argument("file_path", type=click.Path(exists=True, path_type=Path))
def parse(file_path: Path):
    """Parst eine einzelne Spezifikationsdatei."""
    parser = MarkdownParser()
    doc = parser.parse_file(file_path)

    console.print(f"\n[bold]📄 {doc.doc_id}[/bold]")
    console.print(f"   Version: {doc.version}")
    console.print(f"   Layer:   {doc.layer}")
    console.print(f"   Abschnitte: {doc.section_count}")
    console.print(f"   Referenzen: {doc.reference_count}")
    console.print(f"   Tabellen: {len(doc.tables)}")

    if doc.parse_errors:
        console.print(f"\n[yellow]⚠ Parse-Fehler:[/yellow]")
        for error in doc.parse_errors:
            console.print(f"   - {error}")

    # Abschnitte anzeigen
    console.print(f"\n[bold]Abschnitte:[/bold]")
    for section in doc.sections:
        _print_section_tree(section, indent=1)


@main.command()
@click.argument("directory", type=click.Path(exists=True, path_type=Path))
def parse_all(directory: Path):
    """Parst alle MD-Dateien in einem Verzeichnis."""
    parser = MarkdownParser()
    md_files = sorted(directory.rglob("*.md"))

    console.print(f"\n[bold]📂 {directory}[/bold]")
    console.print(f"   Gefundene MD-Dateien: {len(md_files)}\n")

    docs = []
    for file_path in md_files:
        # Archivierte Dateien überspringen
        if "archive" in str(file_path).lower():
            console.print(f"   [dim]⏭ {file_path.name} (archiviert)[/dim]")
            continue

        doc = parser.parse_file(file_path)
        docs.append(doc)

        status = "[green]✓[/green]" if not doc.parse_errors else "[yellow]⚠[/yellow]"
        console.print(
            f"   {status} {doc.doc_id} "
            f"(v{doc.version}, {doc.section_count} Abschnitte, "
            f"{doc.reference_count} Referenzen)"
        )

    console.print(f"\n[bold]Gesamt: {len(docs)} Dokumente geparst[/bold]")


@main.command()
@click.argument("directory", type=click.Path(exists=True, path_type=Path))
def validate(directory: Path):
    """Prüft die Konsistenz aller Spezifikationsdateien."""
    parser = MarkdownParser()
    graph = ReferenceGraph()

    md_files = sorted(directory.rglob("*.md"))
    docs = []

    for file_path in md_files:
        if "archive" in str(file_path).lower():
            continue
        doc = parser.parse_file(file_path)
        docs.append(doc)
        graph.add_document(doc)

    graph.build()

    console.print(f"\n[bold]🔍 Validierung von {len(docs)} Dokumenten[/bold]\n")

    # Broken References
    broken = graph.find_broken_references()
    if broken:
        console.print(f"[red]✗ {len(broken)} gebrochene Referenzen:[/red]")
        for ref in broken[:10]:
            console.print(f"   {ref.source_doc} → {ref.target_doc} (Zeile {ref.line_number})")
        if len(broken) > 10:
            console.print(f"   ... und {len(broken) - 10} weitere")
    else:
        console.print("[green]✓ Keine gebrochenen Referenzen[/green]")

    # CHARTER-Hierarchie
    violations = graph.check_charter_hierarchy()
    if violations:
        console.print(f"\n[red]✗ {len(violations)} CHARTER-Hierarchie-Verstöße:[/red]")
        for v in violations:
            console.print(f"   {v}")
    else:
        console.print("[green]✓ CHARTER-Hierarchie eingehalten[/green]")

    # Parse-Fehler
    total_errors = sum(len(doc.parse_errors) for doc in docs)
    if total_errors > 0:
        console.print(f"\n[yellow]⚠ {total_errors} Parse-Fehler[/yellow]")
    else:
        console.print("[green]✓ Keine Parse-Fehler[/green]")


@main.command()
@click.argument("doc_id")
@click.option("--section", default=None, help="Abschnitts-ID")
@click.argument("directory", type=click.Path(exists=True, path_type=Path))
def impact(directory: Path, doc_id: str, section: str):
    """Impact-Analyse: Was ist betroffen, wenn sich ein Dokument/Abschnitt ändert?"""
    parser = MarkdownParser()
    graph = ReferenceGraph()

    for file_path in sorted(directory.rglob("*.md")):
        if "archive" in str(file_path).lower():
            continue
        doc = parser.parse_file(file_path)
        graph.add_document(doc)

    graph.build()

    affected = graph.impact_analysis(doc_id, section)

    console.print(f"\n[bold]🎯 Impact-Analyse für {doc_id}[/bold]")
    if section:
        console.print(f"   Abschnitt: §{section}")
    console.print(f"\n   Betroffene Dokumente/Abschnitte: {len(affected)}")

    for item in affected:
        console.print(f"   → {item}")


@main.command()
@click.argument("directory", type=click.Path(exists=True, path_type=Path))
def stats(directory: Path):
    """Zeigt Statistiken über den Referenzgraphen an."""
    parser = MarkdownParser()
    graph = ReferenceGraph()

    for file_path in sorted(directory.rglob("*.md")):
        if "archive" in str(file_path).lower():
            continue
        doc = parser.parse_file(file_path)
        graph.add_document(doc)

    graph.build()
    statistics = graph.get_statistics()

    console.print(f"\n[bold]📊 Statistiken[/bold]\n")

    table = Table(show_header=False, box=None)
    table.add_column("Metrik", style="cyan")
    table.add_column("Wert", style="green")

    table.add_row("Dokumente", str(statistics["documents"]))
    table.add_row("Abschnitte", str(statistics["sections"]))
    table.add_row("Referenzen", str(statistics["references"]))
    table.add_row("Cross-Document-Referenzen", str(statistics["cross_document_references"]))
    table.add_row("Cross-Layer-Referenzen", str(statistics["cross_layer_references"]))
    table.add_row("Gebrochene Referenzen", str(statistics["broken_references"]))
    table.add_row("Graph-Knoten", str(statistics["graph_nodes"]))
    table.add_row("Graph-Kanten", str(statistics["graph_edges"]))

    console.print(table)


def _print_section_tree(section, indent=0):
    """Gibt einen Abschnitt als Baum aus."""
    prefix = "  " * indent
    type_badge = f"[dim]({section.section_type.value})[/dim]"
    console.print(f"{prefix}├─ §{section.section_id} {section.title} {type_badge}")
    for child in section.children:
        _print_section_tree(child, indent + 1)


if __name__ == "__main__":
    main()