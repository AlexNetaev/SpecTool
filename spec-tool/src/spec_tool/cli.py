"""
spec-tool CLI — Vollwertiges Kommandozeilen-Tool für das
Spezifikationsmanagement.

Befehle:
    spec-tool parse <datei>              Eine einzelne Datei parsen
    spec-tool parse-all <verzeichnis>    Alle Dateien parsen
    spec-tool validate <verzeichnis>     Konsistenz prüfen
    spec-tool check <datei>              Eine Datei validieren
    spec-tool impact <doc-id>            Impact-Analyse
    spec-tool stats <verzeichnis>        Statistiken anzeigen
    spec-tool graph <verzeichnis>        Referenzgraph anzeigen
    spec-tool roles <verzeichnis>        Rollen auflisten
    spec-tool dataflows <verzeichnis>    Datenflüsse auflisten
    spec-tool generate-views <verz>      Views generieren
    spec-tool verify <verzeichnis>       Vollständige Verifikation
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table as RichTable
from rich.tree import Tree
from rich import box

from spec_tool.parser.md_parser import MarkdownParser
from spec_tool.graph.reference_graph import ReferenceGraph
from spec_tool.validator.consistency import ConsistencyValidator
from spec_tool.generator.views import ViewGenerator

console = Console()
err_console = Console(stderr=True)


# ─────────────────────────────────────────────────────────────
# Hilfsfunktionen
# ─────────────────────────────────────────────────────────────

def find_md_files(directory: Path, exclude_archive: bool = True) -> list[Path]:
    """Findet alle Markdown-Dateien in einem Verzeichnis."""
    if not directory.exists():
        err_console.print(f"[red]Fehler:[/red] Verzeichnis nicht gefunden: {directory}")
        sys.exit(1)

    files = sorted(directory.rglob("*.md"))
    if exclude_archive:
        files = [f for f in files if "archive" not in str(f).lower()]
    return files


def load_documents(directory: Path) -> list:
    """Lädt alle Dokumente aus einem Verzeichnis."""
    parser = MarkdownParser()
    files = find_md_files(directory)
    docs = []
    for f in files:
        try:
            doc = parser.parse_file(f)
            docs.append(doc)
        except Exception as e:
            err_console.print(f"[yellow]Warnung:[/yellow] Fehler beim Parsen von {f}: {e}")
    return docs


def build_graph(docs: list) -> ReferenceGraph:
    """Baut einen Referenzgraphen aus Dokumenten."""
    graph = ReferenceGraph()
    for doc in docs:
        graph.add_document(doc)
    graph.build()
    return graph


def print_doc_summary(doc) -> None:
    """Gibt eine Zusammenfassung eines Dokuments aus."""
    status_icon = "✅" if not doc.parse_errors else "⚠️"
    console.print(f"\n{status_icon} [bold]{doc.doc_id}[/bold]")
    console.print(f"   Version: {doc.version}")
    console.print(f"   Abschnitte: {doc.section_count}")
    console.print(f"   Referenzen: {doc.reference_count}")
    console.print(f"   Tabellen: {len(doc.tables)}")
    if doc.parse_errors:
        for err in doc.parse_errors:
            console.print(f"   [yellow]⚠ {err}[/yellow]")


# ─────────────────────────────────────────────────────────────
# CLI-Hauptgruppe
# ─────────────────────────────────────────────────────────────

@click.group()
@click.version_option(version="0.2.0", prog_name="spec-tool")
def main():
    """
    spec-tool — Parser, Validator und View-Generator für
    strukturierte Spezifikationsdokumente.

    Beispiele:

        spec-tool parse data/foundation/CHARTER.md

        spec-tool validate data/

        spec-tool stats data/

        spec-tool impact foundation/CHARTER.md --directory data/

        spec-tool generate-views data/ --output-dir views/
    """
    pass


# ─────────────────────────────────────────────────────────────
# Befehl: parse
# ─────────────────────────────────────────────────────────────

@main.command()
@click.argument("file_path", type=click.Path(exists=True, path_type=Path))
@click.option("--verbose", "-v", is_flag=True, help="Ausführliche Ausgabe")
def parse(file_path: Path, verbose: bool):
    """Parst eine einzelne Spezifikationsdatei."""
    parser = MarkdownParser()

    with console.status(f"[bold]Parse {file_path.name}...[/bold]"):
        doc = parser.parse_file(file_path)

    print_doc_summary(doc)

    if verbose:
        console.print("\n[bold]Abschnitte:[/bold]")
        for section in doc.sections:
            console.print(f"  §{section.section_id}: {section.title} ({section.section_type.value})")

        if doc.references:
            console.print(f"\n[bold]Referenzen ({len(doc.references)}):[/bold]")
            for ref in doc.references[:20]:
                console.print(f"  → {ref.target_doc} §{ref.target_section or '?'}")

    if doc.parse_errors:
        sys.exit(1)


# ─────────────────────────────────────────────────────────────
# Befehl: parse-all
# ─────────────────────────────────────────────────────────────

@main.command()
@click.argument("directory", type=click.Path(exists=True, path_type=Path))
@click.option("--verbose", "-v", is_flag=True, help="Ausführliche Ausgabe")
def parse_all(directory: Path, verbose: bool):
    """Parst alle Markdown-Dateien in einem Verzeichnis."""
    parser = MarkdownParser()
    files = find_md_files(directory)

    console.print(f"\n[bold]📂 {directory}[/bold]")
    console.print(f"   Gefundene Dateien: {len(files)}\n")

    docs = []
    errors = 0

    for f in files:
        try:
            doc = parser.parse_file(f)
            docs.append(doc)
            icon = "✅" if not doc.parse_errors else "⚠️"
            console.print(
                f"  {icon} {doc.doc_id} "
                f"(v{doc.version}, {doc.section_count} Abschnitte, "
                f"{doc.reference_count} Referenzen)"
            )
            if doc.parse_errors:
                errors += 1
        except Exception as e:
            err_console.print(f"  [red]✗[/red] {f.name}: {e}")
            errors += 1

    console.print(f"\n[bold]Gesamt:[/bold] {len(docs)} Dokumente geparst, {errors} Fehler")

    if verbose:
        for doc in docs:
            if doc.parse_errors:
                print_doc_summary(doc)

    if errors > 0:
        sys.exit(1)


# ─────────────────────────────────────────────────────────────
# Befehl: validate
# ─────────────────────────────────────────────────────────────

@main.command()
@click.argument("directory", type=click.Path(exists=True, path_type=Path))
@click.option("--strict", is_flag=True, help="Bei Warnungen abbrechen")
def validate(directory: Path, strict: bool):
    """Prüft die Konsistenz aller Spezifikationsdokumente."""
    console.print(f"\n[bold]🔍 Validierung von {directory}[/bold]\n")

    docs = load_documents(directory)
    if not docs:
        err_console.print("[red]Keine Dokumente gefunden.[/red]")
        sys.exit(1)

    validator = ConsistencyValidator()

    with console.status("[bold]Validiere...[/bold]"):
        report = validator.validate(docs)

    # Ergebnisse ausgeben
    table = RichTable(box=box.SIMPLE)
    table.add_column("Metrik", style="cyan")
    table.add_column("Wert", style="green")
    table.add_row("Dokumente geprüft", str(report.documents_checked))
    table.add_row("Referenzen geprüft", str(report.references_checked))
    table.add_row("Fehler", f"[{'red' if report.errors else 'green'}]{len(report.errors)}[/]")
    table.add_row("Warnungen", f"[{'yellow' if report.warnings else 'green'}]{len(report.warnings)}[/]")
    table.add_row("Status", f"[{'red' if not report.is_valid else 'green'}]{'UNGÜLTIG' if not report.is_valid else 'GÜLTIG'}[/]")
    console.print(table)

    if report.errors:
        console.print("\n[bold red]Fehler:[/bold red]")
        for r in report.errors:
            console.print(f"  [red]✗ {r.rule_id}[/red] {r.message} ({r.file_path})")

    if report.warnings and (strict or len(report.warnings) <= 20):
        console.print("\n[bold yellow]Warnungen:[/bold yellow]")
        for r in report.warnings:
            console.print(f"  [yellow]⚠ {r.rule_id}[/yellow] {r.message}")

    if not report.is_valid or (strict and report.warnings):
        sys.exit(1)


# ─────────────────────────────────────────────────────────────
# Befehl: check
# ─────────────────────────────────────────────────────────────

@main.command()
@click.argument("file_path", type=click.Path(exists=True, path_type=Path))
def check(file_path: Path):
    """Validiert eine einzelne Datei."""
    parser = MarkdownParser()
    doc = parser.parse_file(file_path)

    validator = ConsistencyValidator()
    report = validator.validate([doc])

    if report.is_valid:
        console.print(f"[green]✅ {file_path.name} ist gültig[/green]")
    else:
        console.print(f"[red]✗ {file_path.name} ist ungültig[/red]")
        for r in report.errors:
            console.print(f"  [red]✗ {r.rule_id}[/red] {r.message}")
        sys.exit(1)


# ─────────────────────────────────────────────────────────────
# Befehl: impact
# ─────────────────────────────────────────────────────────────

@main.command()
@click.argument("doc_id")
@click.option("--section", "-s", default=None, help="Abschnitts-ID")
@click.option("--directory", "-d", type=click.Path(exists=True, path_type=Path), default="data")
def impact(doc_id: str, section: Optional[str], directory: Path):
    """Impact-Analyse: Was ist betroffen, wenn sich ein Dokument ändert?"""
    docs = load_documents(directory)
    graph = build_graph(docs)

    target = f"{doc_id}§{section}" if section else doc_id
    console.print(f"\n[bold]🎯 Impact-Analyse für {target}[/bold]\n")

    affected = graph.impact_analysis(doc_id, section)

    if not affected:
        console.print("[green]Keine betroffenen Dokumente gefunden.[/green]")
        return

    console.print(f"[bold]{len(affected)} betroffene Dokumente/Abschnitte:[/bold]\n")
    for item in affected:
        console.print(f"  → {item}")


# ─────────────────────────────────────────────────────────────
# Befehl: stats
# ─────────────────────────────────────────────────────────────

@main.command()
@click.argument("directory", type=click.Path(exists=True, path_type=Path))
def stats(directory: Path):
    """Zeigt Statistiken über den Referenzgraphen an."""
    docs = load_documents(directory)
    graph = build_graph(docs)
    statistics = graph.get_statistics()

    console.print(f"\n[bold]📊 Statistiken für {directory}[/bold]\n")

    table = RichTable(box=box.ROUNDED)
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

    if statistics["broken_references"] > 0:
        console.print(f"\n[yellow]⚠ {statistics['broken_references']} gebrochene Referenzen gefunden[/yellow]")


# ─────────────────────────────────────────────────────────────
# Befehl: graph
# ─────────────────────────────────────────────────────────────

@main.command()
@click.argument("directory", type=click.Path(exists=True, path_type=Path))
@click.option("--format", "output_format", type=click.Choice(["tree", "list"]), default="tree")
def graph(directory: Path, output_format: str):
    """Zeigt den Referenzgraphen an."""
    docs = load_documents(directory)
    ref_graph = build_graph(docs)

    console.print(f"\n[bold]🔗 Referenzgraph für {directory}[/bold]\n")

    if output_format == "tree":
        tree = Tree("[bold]Dokumente[/bold]")
        for doc in docs:
            doc_node = tree.add(f"[bold]{doc.doc_id}[/bold] (v{doc.version})")
            outgoing = ref_graph.get_outgoing(doc.doc_id)
            for target in outgoing[:10]:
                doc_node.add(f"→ {target}")

        console.print(tree)
    else:
        for doc in docs:
            outgoing = ref_graph.get_outgoing(doc.doc_id)
            incoming = ref_graph.get_incoming(doc.doc_id)
            console.print(f"\n[bold]{doc.doc_id}[/bold]")
            console.print(f"  Ausgehend ({len(outgoing)}):")
            for t in outgoing[:5]:
                console.print(f"    → {t}")
            console.print(f"  Eingehend ({len(incoming)}):")
            for i in incoming[:5]:
                console.print(f"    ← {i}")


# ─────────────────────────────────────────────────────────────
# Befehl: roles
# ─────────────────────────────────────────────────────────────

@main.command()
@click.argument("directory", type=click.Path(exists=True, path_type=Path))
def roles(directory: Path):
    """Listet alle definierten Rollen auf."""
    docs = load_documents(directory)
    generator = ViewGenerator()
    role_views = generator.generate_role_views(docs)

    console.print(f"\n[bold]👥 Rollen ({len(role_views)})[/bold]\n")

    table = RichTable(box=box.ROUNDED)
    table.add_column("Rolle", style="cyan")
    table.add_column("Schicht", style="green")
    table.add_column("LLM", style="yellow")
    table.add_column("Eingänge", style="green")
    table.add_column("Ausgänge", style="green")
    table.add_column("Regeln", style="green")

    for role in role_views:
        table.add_row(
            role.role_id,
            str(role.layer or "?"),
            "Ja" if role.uses_llm else "Nein",
            str(len(role.inputs)),
            str(len(role.outputs)),
            str(len(role.rules)),
        )

    console.print(table)


# ─────────────────────────────────────────────────────────────
# Befehl: dataflows
# ─────────────────────────────────────────────────────────────

@main.command()
@click.argument("directory", type=click.Path(exists=True, path_type=Path))
def dataflows(directory: Path):
    """Listet alle definierten Datenflüsse auf."""
    docs = load_documents(directory)
    generator = ViewGenerator()
    df_views = generator.generate_dataflow_views(docs)

    console.print(f"\n[bold]🔄 Datenflüsse ({len(df_views)})[/bold]\n")

    for df in df_views:
        console.print(f"\n[bold]{df.dataflow_id}[/bold]")
        if df.trigger:
            console.print(f"  Trigger: {df.trigger}")
        if df.steps:
            console.print(f"  Schritte: {len(df.steps)}")
            for i, step in enumerate(df.steps[:5], 1):
                console.print(f"    {i}. {step[:80]}...")


# ─────────────────────────────────────────────────────────────
# Befehl: generate-views
# ─────────────────────────────────────────────────────────────

@main.command()
@click.argument("directory", type=click.Path(exists=True, path_type=Path))
@click.option("--output-dir", "-o", type=click.Path(path_type=Path), default="views")
def generate_views(directory: Path, output_dir: Path):
    """Generiert die rollenzentrierten Views."""
    docs = load_documents(directory)
    generator = ViewGenerator()

    output_dir.mkdir(parents=True, exist_ok=True)

    console.print(f"\n[bold]📝 Generiere Views nach {output_dir}/[/bold]\n")

    # ROLE_VIEWS.md
    role_views = generator.generate_role_views(docs)
    role_md = generator.render_role_views_markdown(role_views)
    role_path = output_dir / "ROLE_VIEWS.md"
    role_path.write_text(role_md, encoding="utf-8")
    console.print(f"  ✅ {role_path} ({len(role_views)} Rollen)")

    # DATAFLOW_MAP.md
    df_views = generator.generate_dataflow_views(docs)
    df_md = generator.render_dataflow_views_markdown(df_views)
    df_path = output_dir / "DATAFLOW_MAP.md"
    df_path.write_text(df_md, encoding="utf-8")
    console.print(f"  ✅ {df_path} ({len(df_views)} Datenflüsse)")

    # TEST_MATRIX.md
    test_entries = generator.generate_test_matrix(docs)
    test_md = generator.render_test_matrix_markdown(test_entries)
    test_path = output_dir / "TEST_MATRIX.md"
    test_path.write_text(test_md, encoding="utf-8")
    console.print(f"  ✅ {test_path} ({len(test_entries)} Test-Einträge)")

    console.print(f"\n[green]Views erfolgreich generiert.[/green]")


# ─────────────────────────────────────────────────────────────
# Befehl: verify (Vollständige Verifikation)
# ─────────────────────────────────────────────────────────────

@main.command()
@click.argument("directory", type=click.Path(exists=True, path_type=Path))
@click.option("--strict", is_flag=True, help="Bei Warnungen abbrechen")
def verify(directory: Path, strict: bool):
    """Vollständige Verifikation: Parse + Validate + Graph + Stats."""
    console.print(Panel("[bold]🔬 Vollständige Verifikation[/bold]", border_style="blue"))

    # Schritt 1: Parse
    console.print("\n[bold]Schritt 1: Parse[/bold]")
    docs = load_documents(directory)
    console.print(f"  {len(docs)} Dokumente geparst")

    # Schritt 2: Validate
    console.print("\n[bold]Schritt 2: Validate[/bold]")
    validator = ConsistencyValidator()
    report = validator.validate(docs)
    console.print(f"  Fehler: {len(report.errors)}")
    console.print(f"  Warnungen: {len(report.warnings)}")
    console.print(f"  Status: {'GÜLTIG' if report.is_valid else 'UNGÜLTIG'}")

    # Schritt 3: Graph
    console.print("\n[bold]Schritt 3: Graph[/bold]")
    ref_graph = build_graph(docs)
    statistics = ref_graph.get_statistics()
    console.print(f"  Knoten: {statistics['graph_nodes']}")
    console.print(f"  Kanten: {statistics['graph_edges']}")
    console.print(f"  Gebrochene Referenzen: {statistics['broken_references']}")

    # Schritt 4: Views (nur zählen, nicht schreiben)
    console.print("\n[bold]Schritt 4: Views (Vorschau)[/bold]")
    generator = ViewGenerator()
    role_views = generator.generate_role_views(docs)
    df_views = generator.generate_dataflow_views(docs)
    test_entries = generator.generate_test_matrix(docs)
    console.print(f"  Rollen: {len(role_views)}")
    console.print(f"  Datenflüsse: {len(df_views)}")
    console.print(f"  Test-Einträge: {len(test_entries)}")

    # Zusammenfassung
    console.print("\n" + "=" * 50)
    all_ok = report.is_valid and statistics["broken_references"] == 0
    if all_ok:
        console.print("[bold green]✅ Verifikation bestanden[/bold green]")
    else:
        console.print("[bold red]✗ Verifikation fehlgeschlagen[/bold red]")
        if report.errors:
            console.print(f"  {len(report.errors)} Fehler")
        if statistics["broken_references"] > 0:
            console.print(f"  {statistics['broken_references']} gebrochene Referenzen")

    if not all_ok or (strict and report.warnings):
        sys.exit(1)


# ─────────────────────────────────────────────────────────────
# Einstiegspunkt
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    main()