from typer import Typer
import typer
from typing_extensions import Annotated

app = Typer(
    name="Knessight Utils",
    no_args_is_help=True,
    help="Utility functions for managing Knessight processes.",
)


@app.command()
def add_job(
    person_id: Annotated[int, typer.Argument()] = None,
    subject: Annotated[str, typer.Argument()] = None,
) -> None:
    """
    Adds a job for a specific person and subject.

    :param person_id: ID of the person.
    :param subject: Subject name.
    """
    if person_id is None:
        person_id = typer.prompt("Person ID", type=int)
    if subject is None:
        subject = typer.prompt("Subject")
    print(f"Adding job for person ID {person_id} and subject '{subject}'")
    raise NotImplementedError("This function is not implemented yet.")


@app.command()
def add_jobs(jobs_file: Annotated[typer.FileText, typer.Argument()] = None) -> None:
    """
    Adds jobs from a specified file.

    :param jobs_file: Path to the file containing job details. format: person_id,subject
    """
    if jobs_file is None:
        jobs_file = typer.prompt("Jobs file", type=typer.FileText)
    print(f"Adding jobs from file: {jobs_file.name}")
    raise NotImplementedError("This function is not implemented yet.")


@app.command()
def get_person_id(query: Annotated[str, typer.Argument()] = None) -> None:
    """
    Prints a list of person IDs based on a query.

    :param query: The query string to search for.
    """
    while query is None:
        query = typer.prompt("Query", type=str)
    print(f"Getting person IDs for query: {query}")
    raise NotImplementedError("This function is not implemented yet.")


@app.command()
def step() -> None:
    """
    Performs a step in the process.
    """
    raise NotImplementedError("This function is not implemented yet.")


if __name__ == "__main__":
    app()
