import sys


#######################################################################
SENTENCES_INPUT = "sentences.txt"
#########################################################################


def filter_sentences_length(input_file: str,
                            output_file: str = SENTENCES_INPUT):
    """
    remove all sentences with fewer than 50 characters,
    :param input_file: Path to the input text file.
    :param output_file: Path to the output text file
    """
    with open(input_file, "r", encoding="utf-8") as infile:
        sentences = infile.readlines()

    # filtered_sentences = [sentence.strip() for sentence in sentences if
    #                       len(sentence.strip()) >= 50]
    filtered_sentences = sentences

    with open(output_file, "w", encoding="utf-8") as outfile:
        outfile.write("\n".join(sentence.strip() for sentence in filtered_sentences))


def assess_relevance(sentences: list[str], keywords: list[str]) -> list[
    int]:
    """Assigns a relevance score (1-5) to each sentence based on
     keyword presence and importance."""

    # Define keyword score mapping based on their position
    score_map = {word: 5 - (i // 2) for i, word in enumerate(keywords)}

    scores = []
    for sentence in sentences:
        unique_keywords = set()  # To ensure each keyword counts only once per sentence
        sentence_score = 1  # Default score

        for word, score in score_map.items():
            if word in sentence and word not in unique_keywords:
                unique_keywords.add(word)
                sentence_score += score - 1  # Convert score to additive format

                if sentence_score >= 5:  # Max possible score
                    sentence_score = 5
                    break

        scores.append(sentence_score)

    return scores

def load_subjects_and_keywords(subjects_file: str, words_file: str) \
        -> dict[str, list[str]]:
    """
    Loads subjects and their corresponding keywords into a dictionary.
    """

    with open(subjects_file, 'r', encoding='utf-8') as s_file:
        subjects = [line.strip() for line in s_file]

    with open(words_file, 'r', encoding='utf-8') as w_file:
        keywords = [line.strip().split() for line in w_file]

    return dict(zip(subjects, keywords))


def main():
    if len(sys.argv) < 4:
        print(
            "Usage: python filter.py subjects.txt words.txt sentences.txt"
            " [outputfile.txt]")
        sys.exit(1)

    subjects_file = sys.argv[1]
    words_file = sys.argv[2]
    sentences_file = sys.argv[3]
    output_file = sys.argv[4] if len(sys.argv) > 4 else "outputfile_filter.txt"

    filter_sentences_length(sentences_file)
    subject_keywords = load_subjects_and_keywords(subjects_file,
                                                  words_file)

    with open(SENTENCES_INPUT, 'r', encoding='utf-8') as s_file:
        sentences = [line.strip() for line in s_file]

    if len(subject_keywords) == 1:
        # Single subject case: write to the output file
        subject = next(iter(subject_keywords))
        results = assess_relevance(sentences, subject_keywords[subject])
        with open(output_file, 'w', encoding='utf-8') as out_file:
            out_file.write("\n".join(map(str, results)) + "\n")
    else:
        # Multiple subjects: create separate files for each
        for subject, keywords in subject_keywords.items():
            results = assess_relevance(sentences, keywords)
            with open(f"{subject.replace(' ', '_')}_assessment.txt", 'w',
                      encoding='utf-8') as out_file:
                out_file.write("\n".join(map(str, results)) + "\n")


if __name__ == "__main__":
    main()
