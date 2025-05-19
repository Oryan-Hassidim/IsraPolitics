"""
בודק אם GPT JOB של פילטר הסתיים, ואם כן מריץ את הפקודה FILTER ויוצר GPT JOB של RANK
פר חכ ונושא
"""
import json
import os
from filter import apply_filter
from gpt_jobs import gpt_activation, retrieve_batch_results
from gpt_jobs import JOBS_DIR, JOBS_DICT_DIR,PROMPTS_DIR,save_job_id


def load_jobs() -> dict:
    if os.path.exists(JOBS_DICT_DIR):
        with open(JOBS_DICT_DIR, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def find_completed_filter_jobs(jobs_dict: dict) -> list[tuple]:
    completed_jobs = []
    for job_id, job_entry in jobs_dict.items():
        if job_entry["type"] == "filter":
            filter_results_path = os.path.join(JOBS_DIR, job_entry["subject"],"filter_output.txt")
            if retrieve_batch_results(job_id, str(filter_results_path)):
                completed_jobs.append((job_entry,str(filter_results_path)))
    return completed_jobs


def create_rank_job(person_id: str, subject: str) -> None:
    # get prompt path
    prompt_path = os.path.join(PROMPTS_DIR, subject, "Rank.txt")
    # activate one gpt job
    input_path = os.path.join(JOBS_DIR,person_id, "texts.txt")
    batch_id = gpt_activation(prompt_path, input_path, "gpt-4.1")
    save_job_id(batch_id, person_id, subject, "rank")


def filter_to_rank():
    jobs_dict = load_jobs()
    completed_filtered_jobs = find_completed_filter_jobs(jobs_dict)
    for job_entry, filter_results_path in completed_filtered_jobs:
        output_path = os.path.join(JOBS_DIR, job_entry["person_id"],job_entry["subject"])
        data_path = os.path.join(JOBS_DIR, job_entry["person_id"])
        for file in ["texts.txt", "ids.txt"]:
            apply_filter(
                filter_results_path,
                str(os.path.join(data_path, file)),
                str(os.path.join(output_path, file))
            )
        create_rank_job(job_entry["person_id"], job_entry["subject"])













