import sqlite3
from gpt_jobs import BASE_DIR
import os
from typing import Any, Tuple, Optional

###########################################################################
# Constants
DB_PATH = os.path.join(BASE_DIR, "Data", "IsraParlTweet.db")
###########################################################################


def load_query(query_path: str) -> str:
    """
    Loads an SQL query from a file.

    This function reads the contents of a file containing an SQL query
    and returns it as a single stripped string.

    :param query_path: Path to the file containing the SQL query.
    :return: The SQL query as a string with leading and trailing whitespace removed.
    """
    with open(query_path, "r", encoding="utf-8") as f:
        return f.read().strip()


def run_query(
    query_path: str, params: Tuple[Any, ...] = (), fetchone: bool = False
) -> Optional[Any]:
    """
    Executes a SQL query and returns results.

    Parameters:
        query_path (str): SQL path to query (can use ? placeholders).
        params (Tuple[Any, ...]): Query parameters.
        fetchone (bool): Whether to fetch only one row.

    Returns:
        Single row (tuple) if fetchone=True,
        List of rows (tuples) otherwise,
        None if nothing found.
    """
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        query = load_query(query_path)
        cursor.execute(query, params)
        if fetchone:
            return cursor.fetchone()
        return cursor.fetchall()


def get_people(query: list[str]) -> None:
    """
    Prints a list of MKs (Members of Knesset) based on the provided query.

    :param query: The query string to search for.
    """
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        conditions = [
            f"(instr(first_name, ?) > 0 OR instr(surname, ?) > 0)" for _ in query
        ]
        sql = f"""
            SELECT *
            FROM people
            WHERE {' AND '.join(conditions)}
            GROUP BY person_id
        """
        params = [word for word in query for _ in range(2)]
        cursor.execute(sql, params)
        results = cursor.fetchall()
        if results:
            print("Found person IDs:")
            for row in results:
                print(f" - {row[0]}")
        else:
            print("No person IDs found.")
