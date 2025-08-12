import sys

from openai import Client
from tqdm import tqdm


def filter(system_prompt_path: str, input_path: str, output_path: str) -> None:
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
    with open("Utils/secrets/OpenAI_key.txt", "r") as file:
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
        # TODO: https://platform.openai.com/docs/guides/batch
        sentences = (line.strip() for line in input_file if line.strip())

        for sentence in tqdm(sentences): # TODO: tqdm
            # prompt = f"{sentence}"
            try:
                response = client.chat.completions.create(
                    model="gpt-4.1-mini",
                    messages=[system_message, {"role": "user", "content": sentence}],
                )
                rating = int(response.choices[0].message.content.strip())
                output_file.write(f"{rating}\n")
                # print(rating)

            except Exception as e:
                print(f"Error processing sentence '{sentence}': {e}")
                output_file.write("Error\n")



if __name__ == "__main__":
    # usage [system_prompt_path] [input_path] [output_path]

    # activate filtering with system args
    filter(sys.argv[1], sys.argv[2], sys.argv[3])