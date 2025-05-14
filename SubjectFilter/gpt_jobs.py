import json
import os
from openai import Client, File
from tqdm import tqdm
from datetime import datetime


def send_job(
    system_prompt_path: str,
    input_path: str,
    output_path: str,
    model: str = "gpt-4.1-mini",
) -> None:
    """
    Filters sentences based on their relevance to a given subject using GPT.
    The system prompt is loaded from a file, and the sentences are read from an input file.
    The results are written to an output file.

    :param system_prompt_path: Path to the system prompt file.
    :param input_path: Path to the input file containing sentences.
    :param output_path: Path to the output file where results will be written.
    :return: None
    """

    # Load api key from the file secrets/OpenAI_key.txt
    with open("secrets/OpenAI_key.txt", "r") as file:
        api_key = file.read().strip()
    client = Client(api_key=api_key)

    # Load system prompt from the file
    with open(system_prompt_path, "r", encoding="utf-8") as file:
        system_prompt = file.read().strip()

    system_message = {"role": "system", "content": system_prompt}

    # Open input file for reading sentences and output file for writing results
    with (
        open(input_path, "r", encoding="utf-8") as input_file,
        open(output_path, "w", encoding="utf-8") as output_file,
    ):
        sentences = (line.strip() for line in input_file if line.strip())

        for sentence in tqdm(sentences):
            # prompt = f"{sentence}"
            try:
                response = client.chat.completions.create(
                    model=model,
                    messages=[system_message, {"role": "user", "content": sentence}],
                )
                rating = int(response.choices[0].message.content.strip())
                output_file.write(f"{rating}\n")
                # print(rating)

            except Exception as e:
                print(f"Error processing sentence '{sentence}': {e}")
                output_file.write("Error\n")


def start_batch_job(
    system_prompt_path: str, input_path: str, model: str = "gpt-4.1-mini"
) -> str:
    """
    creates a batch file for filtering sentences using GPT.
    The system prompt is loaded from a file, and the sentences are read from an input file.

    :param system_prompt_path: Path to the system prompt file.
    :param input_path: Path to the input file containing sentences.

    :return: id of the batch operation
    """
    # Load api key from the file secrets/OpenAI_key.txt
    with open("secrets/OpenAI_key.txt", "r") as file:
        api_key = file.read().strip()
    client = Client(api_key=api_key)

    # Load system prompt from the file
    with open(system_prompt_path, "r", encoding="utf-8") as file:
        system_prompt = file.read().strip()

    system_message = {"role": "system", "content": system_prompt}

    # Open input file for reading sentences and output file for writing results
    with (
        open(input_path, "r", encoding="utf-8") as input_file,
        open("batch_filter.jsonl", "w", encoding="utf-8") as output_file,
    ):
        sentences = (line.strip() for line in input_file if line.strip())

        for i, sentence in tqdm(enumerate(sentences)):
            output_file.write(
                # template:
                # {"custom_id": "request-1", "method": "POST", "url": "/v1/chat/completions", "body": {"model": "gpt-3.5-turbo-0125", "messages": [{"role": "system", "content": "You are a helpful assistant."},{"role": "user", "content": "Hello world!"}],"max_tokens": 1000}}
                # {"custom_id": "request-2", "method": "POST", "url": "/v1/chat/completions", "body": {"model": "gpt-3.5-turbo-0125", "messages": [{"role": "system", "content": "You are an unhelpful assistant."},{"role": "user", "content": "Hello world!"}],"max_tokens": 1000}}
                json.dumps(
                    {
                        "custom_id": f"request-{i}",
                        "method": "POST",
                        "url": "/v1/chat/completions",
                        "body": {
                            "model": model,
                            "messages": [
                                system_message,
                                {"role": "user", "content": sentence},
                            ],
                            "max_tokens": 10_000,
                            "n": 1,
                        },
                    },
                    ensure_ascii=False,
                )
            )
            output_file.write("\n")
        output_file.flush()
        output_file.close()
    with open("batch_filter.jsonl", "rb") as batch_file:
        batch_input_file = client.files.create(file=batch_file, purpose="batch")
        print(batch_input_file)
    os.remove("batch_filter.jsonl")

    batch_input_file_id = batch_input_file.id

    now = datetime.now()
    batch = client.batches.create(
        input_file_id=batch_input_file_id,
        endpoint="/v1/chat/completions",
        completion_window="24h",
        metadata={
            "description": f"Batch filtering sentences {now:%Y-%m-%d %H:%M:%S}",
            "name": f"Batch filtering sentences {now:%Y-%m-%d %H:%M:%S}",
        },
    )
    print(batch)
    return batch.id


def retrieve_batch_results(batch_id: str, output_path: str) -> bool:
    """
    Retrieves the results of a batch operation and writes them to an output file.

    :param batch_id: ID of the batch operation.
    :param output_path: Path to the output file where results will be written.

    :return: True if successful, False otherwise.
    """
    # Load api key from the file secrets/OpenAI_key.txt
    with open("secrets/OpenAI_key.txt", "r") as file:
        api_key = file.read().strip()
    client = Client(api_key=api_key)

    # Get the batch results
    batch_results = client.batches.retrieve(batch_id)
    print(batch_results)
    if not batch_results:
        print("No results found for the given batch ID.")
        return False
    if batch_results.status != "completed":
        print(f"Batch processing not completed. Status: {batch_results.status}")
        return False

    results: dict[int, int | str] = {}

    if batch_results.output_file_id:
        file_response = client.files.retrieve(batch_results.output_file_id)
        if file_response.status == "processed":
            file_content = client.files.content(batch_results.output_file_id)
            # template:
            # {"id": "batch_req_123", "custom_id": "request-2", "response": {"status_code": 200, "request_id": "req_123", "body": {"id": "chatcmpl-123", "object": "chat.completion", "created": 1711652795, "model": "gpt-3.5-turbo-0125", "choices": [{"index": 0, "message": {"role": "assistant", "content": "Hello."}, "logprobs": null, "finish_reason": "stop"}], "usage": {"prompt_tokens": 22, "completion_tokens": 2, "total_tokens": 24}, "system_fingerprint": "fp_123"}}, "error": null}
            # {"id": "batch_req_456", "custom_id": "request-1", "response": {"status_code": 200, "request_id": "req_789", "body": {"id": "chatcmpl-abc", "object": "chat.completion", "created": 1711652789, "model": "gpt-3.5-turbo-0125", "choices": [{"index": 0, "message": {"role": "assistant", "content": "Hello! How can I assist you today?"}, "logprobs": null, "finish_reason": "stop"}], "usage": {"prompt_tokens": 20, "completion_tokens": 9, "total_tokens": 29}, "system_fingerprint": "fp_3ba"}}, "error": null}
            for line in file_content.iter_lines():
                data = json.loads(line)
                custom_id = data["custom_id"]
                rating = int(
                    data["response"]["body"]["choices"][0]["message"]["content"]
                )
                results[int(custom_id[8:])] = rating
        else:
            print(f"Error retrieving file content: {file_response.status}")

    if batch_results.error_file_id:
        error_response = client.files.retrieve(batch_results.error_file_id)
        if error_response.status == "processed":
            error_file_content = client.files.content(batch_results.error_file_id)
            for line in error_file_content.iter_lines():
                error_data = json.loads(line)
                custom_id = error_data["custom_id"]
                error_message = error_data["response"]["body"]["error"]["message"]
                results[int(custom_id[8:])] = error_message
        else:
            print(f"Error retrieving error file: {error_response.status}")

    # Check if the output file already exists
    if os.path.isfile(output_path):
        print(f"Output file '{output_path}' already exists. Deleting it.")
        os.remove(output_path)
    # Check if the output directory exists
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    def fst(item):
        return item[0]

    ordered_results = sorted(results.items(), key=fst)  # Sort by custom_id
    with open(output_path, "w", encoding="utf-8") as output_file:
        for custom_id, rating in ordered_results:
            output_file.write(f"{rating}\n")
    print(f"Batch results written to {output_path}.")

    return True
