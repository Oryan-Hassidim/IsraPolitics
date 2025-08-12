"""
This script is used to filter the results of a previous gpt job and then create a new gpt job for ranking.
It loads the jobs from a JSON file, checks for completed filter jobs, applies the filter to the results, and then creates a new ranking job.
"""
import os

from Utils.gpt_jobs import load_jobs
from filter import apply_filter
from gpt_jobs import safe_batch_start, retrieve_batch_results,delete_job_id
from gpt_jobs import JOBS_DIR, PROMPTS_DIR,save_job_id


def find_completed_filter_jobs(jobs_dict: dict) -> list[tuple]:
    """
       Identifies completed GPT filter jobs based on existing job entries and available results.

       This function iterates over the jobs dictionary and checks for jobs of type "filter".
       For each such job, it verifies whether the filter output file exists and is retrievable
       via `retrieve_batch_results`. If so, it adds the job and its filter output path to the result.

       :param jobs_dict: Dictionary of job metadata indexed by job ID.
       :return: List of tuples where each tuple contains a job entry (dict) and the path to its filter output file.
       """
    completed_jobs = []
    for job_id, job_entry in jobs_dict.items():
        if job_entry["type"] == "filter":
            filter_results_path = os.path.join(JOBS_DIR, job_entry["person_id"], job_entry["subject"],"filter_output.txt")
            if retrieve_batch_results(job_id, str(filter_results_path)):
                completed_jobs.append((job_entry,str(filter_results_path)))
    return completed_jobs


def create_rank_job(person_id: str, subject: str) -> None:
    """
     Creates and starts a GPT ranking job for a given MK and subject.

     This function constructs the appropriate prompt and input paths for the ranking task,
     then starts a GPT batch job and registers the job with a unique ID.

     :param person_id: String ID of the MK (Member of Knesset).
     :param subject: Subject/topic for which to perform the ranking.
     :return: None
     """
    # get prompt path
    prompt_path = os.path.join(PROMPTS_DIR, subject, "rank.txt")
    # activate one gpt job
    input_path = os.path.join(JOBS_DIR,person_id, subject, "texts.txt")
    if os.path.getsize(input_path) == 0:
        print(f"Input file {input_path} is empty. Skipping rank job creation.")
        return
    batch_id = safe_batch_start(prompt_path, input_path, "gpt-4.1")
    save_job_id(batch_id, person_id, subject, "rank")



def filter_to_rank()-> None:
    """
       Transitions completed filter jobs into rank jobs by applying filters and submitting ranking jobs.

       This function:
       - Loads all jobs and finds those with completed filter results.
       - Applies the filter results to both `texts.txt` and `ids.txt`.
       - Starts a GPT ranking job using the filtered data.
       - Deletes the completed filter job entries.

       :return: None
       """
    jobs_dict = load_jobs()
    completed_filtered_jobs = find_completed_filter_jobs(jobs_dict)
    for job_entry, filter_results_path in completed_filtered_jobs:
        output_path = os.path.join(JOBS_DIR, job_entry["person_id"],job_entry["subject"])
        data_path = os.path.join(JOBS_DIR, job_entry["person_id"])
        for file in ["texts.txt", "ids.txt"]:
            if apply_filter(
                filter_results_path,
                str(os.path.join(data_path, file)),
                str(os.path.join(output_path, file))
            ) is False:
                print(f"Failed to apply filter for {job_entry['person_id']} on {job_entry['subject']}")
                return
        create_rank_job(job_entry["person_id"], job_entry["subject"])
    delete_job_id([job_entry["job_id"] for job_entry, _ in completed_filtered_jobs])


if __name__ == "__main__":
    # usage: python filter_to_rank.py
    filter_to_rank()
    # create_rank_job("30788", "התיישבות")











