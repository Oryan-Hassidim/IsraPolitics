"""
מקבל ID של חכ ושם של נושא קיים, יוצר תיקייה אם אין, ומריץ GPT JOB של פילטר
"""
from typing import List, Tuple
import os
import sys
from db_jobs import run_query
from gpt_jobs import safe_batch_start, BASE_DIR, JOBS_DIR, PROMPTS_DIR, save_job_id
####################################################
#constants
SENTENCES_PER_MK_DIR = os.path.join(BASE_DIR, "Utils", "Mk_sentences_query.sql")
########################################


def get_mk_sentences_from_db(mk_id: int) -> List[Tuple[int, str]]:
    """
    Retrieves sentences from the database based on the MK ID.

    :param mk_id: ID of the MK.
    :return: List of tuples containing sentence ID and text.
    """
    rows = run_query(SENTENCES_PER_MK_DIR,(mk_id,))
    # Filter out sentences that are too short
    filtered_rows = [(sentence_id, text) for sentence_id, text in rows if len(text) > 10]
    print(filtered_rows)
    return filtered_rows


def create_filter_job(person_id: str, subject: str) -> None:
    """
    Creates a GPT filter job for a specific MK (Member of Knesset) and subject.

    This function prepares the input data for the filtering task by:
    - Creating an output directory structure for the given MK and subject.
    - Fetching the MK's sentences from the database if this is the first filter for them.
    - Writing the sentence IDs and texts to separate files (`ids.txt` and `texts.txt`).
    - Locating the appropriate filtering prompt.
    - Starting a GPT batch filtering job using the input texts and saving the batch ID.

    :param person_id: String representation of the MK's ID.
    :param subject: Subject or topic for which filtering is being applied.
    :return: None
    """
    # Check if the output directory exists
    output_dir = os.path.join(JOBS_DIR, person_id, subject)
    input_dir = os.path.join(JOBS_DIR, person_id)
    if not os.path.exists(input_dir):
        os.makedirs(input_dir)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    ids_path = os.path.join(input_dir, "ids.txt")
    text_path = os.path.join(input_dir, "texts.txt")
    # if its first filter to this mk, load his sentences from db
    if not os.path.exists(ids_path):
        # save txt files for ids and texts
        sentences = get_mk_sentences_from_db(int(person_id))
        with open(os.path.join(input_dir, "ids.txt"), "w",
                  encoding="utf-8") as f:
            for sentence in sentences:
                f.write(f"{sentence[0]}\n")
        with open(os.path.join(input_dir, "texts.txt"), "w",
                  encoding="utf-8") as f:
            for sentence in sentences:
                f.write(f"{sentence[1]}\n")

    # get prompt path
    prompt_path = os.path.join(PROMPTS_DIR, subject, "Filter.txt")
    # activate one gpt job
    input_path = os.path.join(input_dir, "texts.txt")
    batch_id = safe_batch_start(prompt_path, input_path, "gpt-4.1-mini")
    save_job_id(batch_id, person_id, subject, "filter")


if __name__ == "__main__":
    # usage: python create_filter_job.py <id> <subject>
    if len(sys.argv) != 3:
        print("Usage: python create_filter_job.py <id> <subject>")
        sys.exit(1)
    person_id = sys.argv[1]
    subject = sys.argv[2]
    create_filter_job(person_id, subject)









