"""
runs the whole flow. get file with names of Mks and subjects.
make sure them all ran or run them
"""
import os
from gpt_jobs import BASE_DIR, JOBS_DIR
from db_jobs import run_query
import subprocess

###########################################################################
#constants
SUBJECT_DIR = os.path.join(BASE_DIR, "subjects.txt")
MK_DIR = os.path.join(BASE_DIR, "mks.txt")
MK_NAMES_TO_IDS_DIR = os.path.join(BASE_DIR,"Utils", "names_to_ids.sql")
###########################################################################


def read_subjects_and_mks():
    print(f"reading path {SUBJECT_DIR} for subjects")
    with open(SUBJECT_DIR, "r", encoding="utf-8") as file:
        subjects = [line.strip() for line in file if line.strip()]
    print(f"reading path {MK_DIR} for Mk's names")
    with open(MK_DIR, "r", encoding="utf-8") as file:
        mks = [line.strip() for line in file if line.strip()]
    return subjects, mks


def get_mk_ids(mk_names: list[str])->list[str]:
    print("getting mk ids by names from db:")
    ids = []
    for name in mk_names:
        id  = str(run_query(MK_NAMES_TO_IDS_DIR,(name,)))
        if id == "[]":
            print(f"name {name} does not exist")
            continue
        ids.append(id)


    return ids


def check_if_pair_exist(mk_id:str, subject:str)->bool:
    pair_dir = os.path.join(JOBS_DIR, mk_id, subject)
    ids_path = os.path.join(pair_dir, "ids.txt")
    texts_path = os.path.join(pair_dir, "texts.txt")
    return os.path.isfile(ids_path) and os.path.isfile(texts_path)


def check_and_confirm_pairs(mk_ids, subjects) -> list[tuple[str, str]]:
    """Check for existing mk-subject pairs and ask user whether to replace or ignore them.
    Returns a list of (mk_id, subject) pairs to process.
    """
    confirmed_pairs = []
    # Ask user up front how to handle existing pairs
    while True:
        global_choice = input(
            "Handle existing pairs:\n"
            "  [r] Replace All\n"
            "  [i] Ignore All\n"
            "  [a] Ask per pair\n"
            "Choose an option: "
        ).strip().lower()

        if global_choice in {"r", "i", "a"}:
            break
        else:
            print("Invalid input. Please enter 'r', 'i', or 'a'.")

    for mk_id in mk_ids:
        for subject in subjects:
            files_exist = check_if_pair_exist(mk_id,subject)
            if files_exist:
                if global_choice == "r":
                    confirmed_pairs.append((mk_id, subject))
                elif global_choice == "i":
                    continue
                else:  # Ask per pair
                    while True:
                        choice = input(f"Pair exists for MK {mk_id} and subject '{subject}'. Replace (r) or Ignore (i)? ").strip().lower()
                        if choice == 'r':
                            confirmed_pairs.append((mk_id, subject))
                            break
                        elif choice == 'i':
                            break
                        else:
                            print("Invalid input. Please enter 'r' or 'i'.")
            else:
                confirmed_pairs.append((mk_id, subject))  # Add if no existing files
    return confirmed_pairs


def check_for_prompt(subjects:list[str]):
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
        subprocess.run(["python", "create_filter_job.py", mk_id, subject])


if __name__ == "__main__":
    main()




