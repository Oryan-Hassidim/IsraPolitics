from typer import Typer
import typer

app = Typer(
    name="Knessight Utils",
    no_args_is_help=True,
    help="Utility functions for managing Knessight processes.",
)


@app.command()
def add_job(
    person_id: int = typer.Option(..., prompt="Person ID"),
    subject: str = typer.Option(..., prompt="Subject"),
) -> None:
    """
    Adds a job for a specific person and subject.

    :param person_id: ID of the person.
    :param subject: Subject name.
    """
    raise NotImplementedError("This function is not implemented yet.")


@app.command()
def add_jobs(jobs_file: str) -> None:
    """
    Adds jobs from a specified file.

    :param jobs_file: Path to the file containing job details. format: person_id,subject
    """
    raise NotImplementedError("This function is not implemented yet.")


@app.command()
def get_person_ids(query: str = typer.Option(..., prompt="Query")) -> None:
    """
    Prints a list of person IDs based on a query.

    :param query: The query string to search for.
    """
    raise NotImplementedError("This function is not implemented yet.")


@app.command()
def step() -> None:
    """
    Performs a step in the process.
    """
    raise NotImplementedError("This function is not implemented yet.")


if __name__ == "__main__":
    app()
