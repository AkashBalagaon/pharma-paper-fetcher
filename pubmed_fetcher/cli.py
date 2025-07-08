import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import typer
from pubmed_fetcher import fetcher

app = typer.Typer()

@app.command()
def get_papers_list(
    query: str,
    file: str = typer.Option(None, "--file", "-f", help="Filename to save results as CSV"),
    debug: bool = typer.Option(False, "--debug", "-d", help="Enable debug logging"),
):
    if debug:
        import logging
        logging.basicConfig(level=logging.INFO)

    typer.echo(f"Running query: {query}")

    try:
        ids = fetcher.fetch_pubmed_ids(query)
        papers = fetcher.fetch_pubmed_details(ids)

        if file:
            fetcher.save_to_csv(papers, file)
            typer.echo(f"Results saved to {file}")
        else:
            from rich.console import Console
            from rich.table import Table

            console = Console()
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("PubmedID", width=10)
            table.add_column("Title", width=50)
            table.add_column("Non-academic Author(s)")
            table.add_column("Company Affiliation(s)")
            table.add_column("Email")

            for paper in papers:
                table.add_row(
                    paper["PubmedID"],
                    paper["Title"],
                    paper["Non-academic Author(s)"],
                    paper["Company Affiliation(s)"],
                    paper["Corresponding Author Email"]
                )
            console.print(table)

    except Exception as e:
        typer.echo(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    app()
