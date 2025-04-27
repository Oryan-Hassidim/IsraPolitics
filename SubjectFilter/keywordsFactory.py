from openai import OpenAI
import sys


###########################################################################

CLIENT = OpenAI(
    api_key="sk-proj-zAvav4v8nYZQDwRKT0eJKzKZVBSLQOyHwlkctTyfKQ3goRRkJZP68"
            "WqvtGtYi_X6watvbaWoRZT3BlbkFJDF4OLC4_Wq9yDh1lJvy5TnLWSl7a8-0P"
            "JD1dKP6KMhizitkkmLNYs9rLY7mY56CEsg7bXNQf0A"
)

OUTPUTFILE = "keywords.txt"
INPUTFILE = "subjects.txt"
###########################################################################


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
            "You are an AI language expert specializing in keyword "
            "extraction and text classification. "
            "Your task is to generate a list of 10 keywords that best "
            "determine whether a sentence "
            "is related to a given subject.\n\n"
            "The keywords should:\n"
            "1. Be common indicators of relevance to the subject.\n"
            "2. Include synonyms or variations if necessary.\n"
            "3. Avoid overly generic words that are not useful for "
            "classification.\n\n"
            "4. **Order the keywords by importance**, most"
            "representative keywords first."
            "Your response should be a **comma-separated list of"
            " keywords** (each keyword- a single word). "
        )
    }


def get_keywords(subjects: list[str]) -> dict[str, list[str]]:
    """
    Uses GPT to generate 5-10 keywords that determine if a sentence is
     about the given subjects.

    Parameters:
    - subjects (list[str]): A list of subjects for which to extract
     keywords.

    Returns:
    - dict[str, list[str]]: A dictionary where each subject maps to a
    list of extracted keywords.
    """
    system_message = create_system_message()
    results = {}

    for subject in subjects:
        prompt = f"Subject: {subject}\nGenerate 5-10 keywords that " \
                 f"indicate a sentence is about this subject."

        try:
            response = CLIENT.chat.completions.create(
                model="gpt-4o",
                messages=[system_message,
                          {"role": "user", "content": prompt}]
            )

            keywords = response.choices[0].message.content.strip()
            keyword_list = [kw.strip() for kw in keywords.split(",")]
            results[subject] = keyword_list

        except Exception as e:
            print(f"Error processing subject '{subject}': {e}")
            results[subject] = []  # Store an empty list in case of failure

    return results


def get_inflections(keywords_dict: dict[str, list[str]]) -> dict[str, list[str]]:
    """
    Uses GPT to generate inflected forms for each keyword in the given dictionary.

    Parameters:
    - keywords_dict (dict[str, list[str]]): A dictionary where each key is a subject
      and the value is a list of keywords.

    Returns:
    - dict[str, list[str]]: A dictionary where each subject maps to a list of
      inflected forms of the original keywords.
    """
    results = {}

    for subject, keywords in keywords_dict.items():
        results[subject] = []

        for keyword in keywords:
            prompt = f"Generate 5 common Hebrew inflections of the word '{keyword}', " \
                     f"including different verb conjugations, tenses, and plural forms. " \
                     f"Return only the words as a comma-separated list."

            try:
                response = CLIENT.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "system", "content": "You are a Hebrew linguistic assistant."},
                              {"role": "user", "content": prompt}]
                )

                inflections = response.choices[0].message.content.strip()
                inflection_list = [word.strip() for word in inflections.split(",")]
                results[subject].extend(inflection_list)

            except Exception as e:
                print(f"Error processing keyword '{keyword}' in subject '{subject}': {e}")
                results[subject].append(keyword)  # Fallback to original keyword if failure

    return results


def main() -> None:
    """
    Main function to read subjects from an input file, generate keywords
     using GPT,
    and write the keywords to an output file.

    Command-line Usage:
    python keywordsFactory.py [input_file] [output_file]

    If no input file is provided, it defaults to "subjects.txt".
    If no output file is provided, it defaults to "keywords.txt".

    Parameters:
    - None

    Returns:
    - None
    """

    # Read command-line arguments
    args = sys.argv[1:]

    # Determine input and output files based on user input
    if len(args) >= 1:
        input_file = args[0]
    else:
        input_file = INPUTFILE  # Use default input file

    if len(args) >= 2:
        output_file = args[1]
    else:
        output_file = OUTPUTFILE  # Use default output file

    try:
        # Read subjects from the input file
        with open(input_file, 'r', encoding='utf-8') as file:
            subjects = [line.strip() for line in file if line.strip()]

        if not subjects:
            print("Error: Input file is empty.")
            return

        # Generate keywords for each subject
        keywords_dict = get_keywords(subjects)
        #keywords_dict = get_inflections(keywords_dict)

        # Write keywords to the output file
        with open(output_file, 'w', encoding='utf-8') as file:
            for subject in subjects:
                keywords = " ".join(keywords_dict.get(subject, []))
                file.write(keywords + "\n")

        print(f"Keywords successfully written to {output_file}")

    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
