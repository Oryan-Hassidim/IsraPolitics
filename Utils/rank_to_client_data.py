"""
בודק אם נגמר הגוב של RANK ואם כן יוצר CSV של קליינט דאטה
"""

import os
import sys
import json
from gpt_jobs import JOBS_DIR,retrieve_batch_results,delete_job_id,load_jobs, BASE_DIR
import sqlite3
from typing import List, Tuple
from db_jobs import run_query


#######################################################
# Constants
CLIENT_DIR = os.path.join(BASE_DIR, "Client", "client_data","mk_data" )
#######################################################




def get_metadata_for_id(query_path: str, speech_id: int) -> Tuple[str, str]:
    """Executes query with given ID, returns (date, topic)"""
    result = run_query(query_path,(speech_id,))
    return result if result else ("UNKNOWN_DATE", "UNKNOWN_TOPIC")


def load_ranked_data_with_metadata(ids_file: str, sentences_file: str,
        ranks_file: str,query_path: str) \
        -> List[Tuple[int, str, str, str, int]]:

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
    completed_jobs = []
    for job_id, job_entry in jobs_dict.items():
        if job_entry["type"] == "rank":
            filter_results_path = os.path.join(JOBS_DIR, job_entry["subject"],"filter_output.txt")
            if retrieve_batch_results(job_id, str(filter_results_path)):
                completed_jobs.append((job_entry,str(filter_results_path)))
    return completed_jobs


def create_client_data_csv(person_id: str, subject: str) -> None:
    """
    Create a CSV file for client data based on the rank job results.
    """
    # Check if the output directory exists
    output_dir = os.path.join(JOBS_DIR, person_id, subject)
    if not os.path.exists(output_dir):
        print("Output directory does not exist.")
        return
    csv_path = os.path.join(CLIENT_DIR, person_id, f"{subject}.csv")
    # Check if the CSV file already exists, and weather to overwrite it
    if os.path.isfile(csv_path):
        print(f"Output file '{csv_path}' already exists. override? y/n.")
        override = input().strip().lower()
        if override != "y":
            print("Exiting without creating CSV.")
            return

    # Create the CSV file
    with open(csv_path, "w", encoding="utf-8") as csv_file:
        csv_file.write("Id, Date, Topic,Text,Rank\n")
        # for each line in the filter output file, get the corresponding
        # text,id,rank, and extract date and topic from db
        rows = load_ranked_data_with_metadata(
            os.path.join(output_dir, "ids.txt"),
            os.path.join(output_dir, "texts.txt"),
            os.path.join(output_dir, "ranks.txt"),
            os.path.join(BASE_DIR, "date_topic_per_sentence_id.sql")
        )
        for speech_id, date, topic, text, rank in rows:
            csv_file.write(f"{speech_id}, {date}, {topic}, {text}, {rank}\n")



def rank_to_client_data():
    jobs_dict = load_jobs()
    completed_rank_jobs = find_completed_rank_jobs(jobs_dict)
    for job_entry, filter_results_path in completed_rank_jobs:
        create_client_data_csv(job_entry["person_id"], job_entry["subject"])
    delete_job_id([job_entry["job_id"] for job_entry, _ in completed_rank_jobs])



if __name__ == "__main__":
    # usage: python rank_to_client_data.py
    rank_to_client_data()