"""
runs the whole flow. get file with names of Mks and subjects.
make sure them all ran or run them
"""
import os
from gpt_jobs import BASE_DIR, JOBS_DIR
from db_jobs import run_query
import subprocess
from typing import List, Tuple


###########################################################################
#constants
SUBJECT_DIR = os.path.join(BASE_DIR, "subjects.txt")
MK_DIR = os.path.join(BASE_DIR, "mks.txt")
MK_NAMES_TO_IDS_DIR = os.path.join(BASE_DIR,"Utils", "names_to_ids.sql")
###########################################################################


def read_subjects_and_mks() -> Tuple[List[str], List[Tuple[str, str]]]:
    """
    Reads subjects and MK names from predefined text files.

    - `SUBJECT_DIR` is expected to contain one subject per line.
    - `MK_DIR` is expected to contain MK names (at least two words per line).
    - For each MK name, all possible (first_name, last_name) splits are generated.

    :return: A tuple:
        - List of subject strings.
        - List of tuples representing possible (first_name, last_name) combinations.
    """
    print(f"reading path {SUBJECT_DIR} for subjects")
    with open(SUBJECT_DIR, "r", encoding="utf-8") as file:
        subjects = [line.strip() for line in file if line.strip()]

    print(f"reading path {MK_DIR} for MK's names")
    with open(MK_DIR, "r", encoding="utf-8") as file:
        raw_mks = [line.strip() for line in file if line.strip()]

    # For each MK name, generate all (first_name, last_name) possibilities
    mk_splits = []
    for name in raw_mks:
        parts = name.split()
        if len(parts) < 2:
            print(f"Skipping name '{name}' (not enough parts)")
            continue
        for i in range(1, len(parts)):
            first = " ".join(parts[:i])
            last = " ".join(parts[i:])
            mk_splits.append((first, last))

    return subjects, mk_splits



def get_mk_ids(mk_names: list[tuple[str, str]]) -> list[str]:
    """
    Retrieves MK IDs from the database based on their first and last names.

    Executes a query for each name tuple. If a match is found, the MK's ID is added to the result.

    :param mk_names: List of (first_name, last_name) tuples.
    :return: List of MK IDs as strings.
    """
    print("getting mk ids by names from db:")
    ids = []
    for first_name, surname in mk_names:
        result = run_query(MK_NAMES_TO_IDS_DIR, (first_name, surname))
        if not result or not result[0]:
            print(f"name {first_name} {surname} does not exist")
            continue
        person_id = str(result[0][0])  # Get the integer from [(482,)]
        ids.append(person_id)
    return ids


def check_if_pair_exist(mk_id:str, subject:str)->bool:
    """
    Checks whether both 'ids.txt' and 'texts.txt' exist for the given MK-subject pair.

    :param mk_id: MK's ID.
    :param subject: Subject name.
    :return: True if both files exist, False otherwise.
    """
    pair_dir = os.path.join(JOBS_DIR, mk_id, subject)
    ids_path = os.path.join(pair_dir, "ids.txt")
    texts_path = os.path.join(pair_dir, "texts.txt")
    return os.path.isfile(ids_path) and os.path.isfile(texts_path)


def check_and_confirm_pairs(mk_ids, subjects) -> list[tuple[str, str]]:
    """



def check_for_prompt(subjects: List[str]) -> List[str]:
    """
    Verifies that prompt files exist for each subject.

    Each subject is expected to have:
    - `filter.txt` and `rank.txt` files located in its prompt directory.

    :param subjects: List of subject names.
    :return: List of subjects that have both required prompt files.
    """
    prompts_exist = []
    for subject in subjects:
        directory = os.path.join(BASE_DIR, "Prompts", subject)
        ids_path = os.path.join(directory, "filter.txt")
        texts_path = os.path.join(directory, "rank.txt")
        if os.path.isfile(ids_path) and os.path.isfile(texts_path):
            prompts_exist.append(subject)
        else:
            print(f"{subject} has no prompts\n")
    return prompts_exist


def main():
    print("running filter_to_rank.py")
    subprocess.run(["python", "filter_to_rank.py"])
    print("rank_to_client_data.py")
    subprocess.run(["python", "rank_to_client_data.py"])

    subjects, mks = read_subjects_and_mks()
    mk_ids = get_mk_ids(mks)
    subjects_with_prompts = check_for_prompt(subjects)
    pairs_for_jobs = check_and_confirm_pairs(mk_ids, subjects_with_prompts)
    for mk_id, subject in pairs_for_jobs:
        print(f"Creating filter job for MK {mk_id} and subject '{subject}'")
        subprocess.run(["python", "create_filter_job.py", mk_id, subject])


if __name__ == "__main__":
    main()




