"""
בודק אם נגמר הגוב של RANK ואם כן יוצר CSV של קליינט דאטה
"""

import os
from gpt_jobs import JOBS_DIR,retrieve_batch_results,delete_job_id,load_jobs, BASE_DIR
from typing import List, Tuple
from db_jobs import run_query
import csv

#######################################################
# Constants
CLIENT_DIR = os.path.join(BASE_DIR, "Client", "client_data","mk_data" )
#######################################################


def get_metadata_for_id(query_path: str, speech_id: int) -> Tuple[str, str]:
    """
    Executes a SQL query to retrieve the date and topic for a given speech ID.

    :param query_path: Path to the SQL query file.
    :param speech_id: Speech ID to query.
    :return: Tuple of (date, topic) if found, otherwise ("UNKNOWN_DATE", "UNKNOWN_TOPIC").
    """
    result = run_query(query_path,(speech_id,))
    if result and len(result[0]) == 2:
        return result[0]
    return ("UNKNOWN_DATE", "UNKNOWN_TOPIC")


def load_ranked_data_with_metadata(ids_file: str, sentences_file: str,
        ranks_file: str,query_path: str) \
        -> List[Tuple[int, str, str, str, int]]:
    """
    Loads speech IDs, texts, and ranks from files and enriches them with metadata (date, topic).

    :param ids_file: Path to the file containing speech IDs.
    :param sentences_file: Path to the file containing speech texts.
    :param ranks_file: Path to the file containing ranks.
    :param query_path: Path to the SQL query file for retrieving metadata.
    :return: List of tuples (speech_id, date, topic, text, rank).
    :raises ValueError: If the input files have mismatched lengths.
    """

    with open(ids_file, "r", encoding="utf-8") as f_ids, \
            open(sentences_file, "r", encoding="utf-8") as f_texts, \
            open(ranks_file, "r", encoding="utf-8") as f_ranks:

        ids = [int(line.strip()) for line in f_ids]
        texts = [line.strip() for line in f_texts]
        ranks = [int(line.strip()) for line in f_ranks]

    if not (len(ids) == len(texts) == len(ranks)):
        raise ValueError("Mismatch in file lengths: ids, texts, or ranks")

    results = []
    for speech_id, text, rank in zip(ids, texts, ranks):
        date, topic = get_metadata_for_id(query_path, speech_id)
        results.append((speech_id, date, topic, text, rank))

    return results


def find_completed_rank_jobs(jobs_dict: dict) -> list[tuple]:
    """
    Finds completed rank jobs by checking for available filter output files.

    :param jobs_dict: Dictionary of job metadata entries.
    :return: List of tuples (job_entry, path_to_filter_output) for completed rank jobs.
    """
    completed_jobs = []
    for job_id, job_entry in jobs_dict.items():
        if job_entry["type"] == "rank":
            filter_results_path = os.path.join(JOBS_DIR, job_entry["subject"],job_entry["person_id"], "filter_output.txt")
            if retrieve_batch_results(job_id, str(filter_results_path)):
                completed_jobs.append((job_entry,str(filter_results_path)))
    return completed_jobs


def create_client_data_csv(person_id: str, subject: str) -> None:
    """
    Creates a CSV file containing enriched ranked data (with metadata) for a specific MK and subject.

    - Extracts ranked sentences from existing filter output.
    - Retrieves date and topic metadata from the database.
    - Saves the result as a CSV in the client directory.

    :param person_id: ID of the MK.
    :param subject: Subject name.
    """
    # Check if the output directory exists
    output_dir = os.path.join(JOBS_DIR, person_id, subject)
    if not os.path.exists(output_dir):
        print("Output directory does not exist.")
        return
    os.makedirs(os.path.join(CLIENT_DIR, person_id), exist_ok=True)
    csv_path = os.path.join(CLIENT_DIR, person_id, f"{subject}.csv")
    # Check if the CSV file already exists, and weather to overwrite it
    if os.path.isfile(csv_path):
        print(f"Output file '{csv_path}' already exists. override? y/n.")
        override = input().strip().lower()
        if override != "y":
            print("Exiting without creating CSV.")
            return

    # Create the CSV file
    with open(csv_path, "w", encoding="utf-8",newline='') as csv_file:
        writer = csv.writer(csv_file, quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["Id", "Date", "Topic", "Text", "Rank"])
        # for each line in the filter output file, get the corresponding
        # text,id,rank, and extract date and topic from db
        rows = load_ranked_data_with_metadata(
            os.path.join(output_dir, "ids.txt"),
            os.path.join(output_dir, "texts.txt"),
            os.path.join(JOBS_DIR,subject, person_id, "filter_output.txt"),
            os.path.join(BASE_DIR,"Utils", "date_topic_per_sentence_id.sql")
        )
        for speech_id, date, topic, text, rank in rows:
            writer.writerow([speech_id, date, topic, text, rank])



def rank_to_client_data():
    """
    Processes all completed rank jobs and creates a CSV output for each.

    - Loads job metadata.
    - Identifies completed rank jobs.
    - Generates client-ready CSVs for each.
    - Deletes the processed job entries from the jobs file.
    """
    jobs_dict = load_jobs()
    completed_rank_jobs = find_completed_rank_jobs(jobs_dict)
    for job_entry, filter_results_path in completed_rank_jobs:
        create_client_data_csv(job_entry["person_id"], job_entry["subject"])
    delete_job_id([job_entry["job_id"] for job_entry, _ in completed_rank_jobs])



if __name__ == "__main__":
    # usage: python rank_to_client_data.py
    rank_to_client_data()