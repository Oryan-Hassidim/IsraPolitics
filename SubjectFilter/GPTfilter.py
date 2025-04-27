from openai import OpenAI
import sys

###########################################################################

CLIENT = OpenAI(
    api_key="sk-proj-zAvav4v8nYZQDwRKT0eJKzKZVBSLQOyHwlkctTyfKQ3goRRkJZP68"
            "WqvtGtYi_X6watvbaWoRZT3BlbkFJDF4OLC4_Wq9yDh1lJvy5TnLWSl7a8-0P"
            "JD1dKP6KMhizitkkmLNYs9rLY7mY56CEsg7bXNQf0A"
)

INPUTFILE = "subjects.txt"
###########################################################################

# 1st try
# def create_system_message() -> dict:
#     """
#     Creates a system message for the GPT model to evaluate sentences based
#     on relevance to the given topic.
#     Returns:
#     - dict: A system message with the content about the topic for GPT model
#     """
#     return {
#   "role": "system",
#   "content": (
#     "You are an researcher of Israeli politics. you need to asses the contribution of a sentence, to study a specific issue."
#     "You will be given a sentence, "
#     "and your task is to evaluate if this including this sentence, will contribute."
#     "Rate the connection on a scale from 1 to 5, where:\n"
#     "1 = Not related at all, or not enough information(for example, sentence like 'i agree!' is 1\n"
#     "2 = probably not related\n"
#     "3 = maybe related\n"
#     "4 = probably related\n"
#     "5 = the sentence is about this issue, or Directly and clearly related\n\n"
#     "Only return the number (1 to 5) as your response."
#
#   )
#
# }   90% catch, 256 unrelated.

#2nd try
# def create_system_message() -> dict:
#     """
#     Creates a system message for the GPT model to evaluate sentences based
#     on relevance to the given topic.
#     Returns:
#     - dict: A system message with the content about the topic for GPT model
#     """
#     return {
#   "role": "system",
#   "content": (
#     "You are an researcher of Israeli politics. you need to asses the contribution of a sentence, to study a specific issue."
#     "You will be given a sentence, "
#     "and your task is to evaluate if this including this sentence, will contribute."
#     "Rate the connection on a scale from 1 to 5, where:\n"
#     "1 = Not related at all, or not enough information(for example, sentence like 'i agree!' is 1\n"
#     "2 = probably not related\n"
#     "3 = maybe related\n"
#     "4 = probably related\n"
#     "5 = the sentence is about this issue, or Directly and clearly related\n\n"
#     "note: we prefer to give a non related higher score, then give related lower score(up to reason)!"
#     "Only return the number (1 to 5) as your response."
#
#   )
#
# }


def create_system_message() -> dict:
    """
    Creates a system message for the GPT model to evaluate sentences based
    on relevance to the given topic.
    Returns:
    - dict: A system message with the content about the topic for GPT model
    """
    return {
  "role": "system",
  "content": (
    "You are an researcher of Israeli politics. you need to asses the contribution of a sentence, to study opinios of politicians on specific issue."
    "You will be given a sentence, "
    "and your task is to evaluate if including this sentence, will contribute."
    "Rate the connection on a scale from 1 to 5, where: 1 is not related, and 5 is 'this is definnately sentenct to be included about this issue.\n"
    "note: we prefer to be wrong slightly up, than slightly down"
    "Only return the number (1 to 5) as your response."

  )

}


def asses_connection(subject: str, sentences: list[str]) -> list[int]:
    """
    Assesses the relevance of each sentence to a given subject.
    Returns a list of integers from 1 to 5 representing the relevance.
    """
    system_message = create_system_message()
    results = []

    for sentence in sentences:
        prompt = (f"the subject: '{subject}'\n"
                  f"Sentence: {sentence}\nOnly reply with a number between 1 and 5.")

        try:
            response = CLIENT.chat.completions.create(
                model="gpt-4o",
                messages=[system_message,
                          {"role": "user", "content": prompt}]
            )
            rating = int(response.choices[0].message.content.strip())
            results.append(rating)
            print(rating)

        except Exception as e:
            print(f"Error processing sentence '{sentence}': {e}")
            results.append(None)

    return results



def main():
    if len(sys.argv) < 3:
        print("Usage: python GPTfilter.py sentences.txt subjects.txt [output_dir/]")
        sys.exit(1)

    sentences_file = sys.argv[1]
    subjects_file = sys.argv[2]

    # Load all sentences
    with open(sentences_file, 'r', encoding='utf-8') as s_file:
        sentences = [line.strip() for line in s_file if line.strip()]

    # Load all subjects
    with open(subjects_file, 'r', encoding='utf-8') as subj_file:
        subjects = [line.strip() for line in subj_file if line.strip()]

    for subject in subjects:
        results = asses_connection(subject, sentences)
        output_path = "temp_output.txt"

        with open(output_path, 'w', encoding='utf-8') as out_file:
            out_file.write("\n".join(str(r) if r is not None else "Error" for r in results))




if __name__ == "__main__":
    main()