import sys
from filter import main as filter_main
from collections import defaultdict
from GPTfilter import main as GPTmain  # Import the function directly
import pandas as pd


def load_manual_outputs(file_path: str) -> list[int]:
    """Loads the expected manual outputs from a file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return [int(line.strip()) for line in file]


def load_predicted_outputs(output_file: str) -> list[int]:
    """Loads the predicted outputs from the generated assessment file."""
    with open(output_file, 'r', encoding='utf-8') as file:
        return [int(line.strip()) for line in file]


def evaluate_accuracy(manual_outputs: list[int],
                      predicted_outputs: list[int]):
    """
    Evaluates prediction performance as a percentage confusion matrix,
    including per-label accuracy (row-wise accuracy).
    """
    num_labels = 5  # assuming labels 1 through 5
    confusion = defaultdict(lambda: defaultdict(int))
    total_per_label = defaultdict(int)
    correct_sentences = []
    mistaken_sentences = []

    for i, (manual, predicted) in enumerate(zip(manual_outputs, predicted_outputs)):
        confusion[manual][predicted] += 1
        total_per_label[manual] += 1
        if manual == predicted:
            correct_sentences.append(i)
        else:
            mistaken_sentences.append(i)

    # Save correct/mistaken indexes
    with open("correct_sentences.txt", 'w', encoding='utf-8') as correct_file:
        correct_file.write("\n".join(map(str, correct_sentences)) + "\n")

    with open("mistaken_sentences.txt", 'w', encoding='utf-8') as mistaken_file:
        mistaken_file.write("\n".join(map(str, mistaken_sentences)) + "\n")

    # Print table header
    print("Confusion Matrix (percentages):")
    header = ["Actual \\ Pred"] + [str(i) for i in range(1, num_labels + 1)] + ["Accuracy"]
    print("\t".join(header))

    # Print matrix rows
    for actual in range(1, num_labels + 1):
        row = [str(actual)]
        total = total_per_label[actual]
        correct = confusion[actual][actual]
        for pred in range(1, num_labels + 1):
            count = confusion[actual][pred]
            percent = (count / total * 100) if total else 0.0
            row.append(f"{percent:.1f}%")
        accuracy = (correct / total * 100) if total else 0.0
        row.append(f"{accuracy:.1f}%")
        print("\t".join(row))



def divide_to_files(manual_outputs, predicted_outputs, sentences_file,
                    correct_file='correct.xlsx', wrong_file='wrong.xlsx'):
    # Read sentences (UTF-8-safe)
    with open(sentences_file, 'r', encoding='utf-8') as s_file:
        sentences = [line.strip() for line in s_file]

    fours_and_fives = 0
    caught = 0
    correct_rows = []
    wrong_rows = []
    ones = 0
    wrongsT = 0

    for sentence, manual, predicted in zip(sentences, manual_outputs, predicted_outputs):
        if predicted == 4 or predicted == 5:
            if  manual == 1 or manual == 2:
                wrongsT += 1
        if predicted == 1:
            ones += 1
        if manual == 4 or manual == 5:
            fours_and_fives +=1
            if predicted == 4 or predicted == 5 :
                caught += 1
        if manual == predicted or (manual == 4 and predicted == 5) or (manual == 5 and predicted == 4) \
                or (manual == 1 and predicted == 2)or (manual == 2 and predicted == 1):
            correct_rows.append([sentence, predicted])
        else:
            wrong_rows.append([sentence, manual, predicted])

    # Convert to DataFrames (pandas handles Hebrew perfectly)
    correct_df = pd.DataFrame(correct_rows, columns=["משפט", "פלט נכון"])  # "Sentence", "Correct Output"
    wrong_df = pd.DataFrame(wrong_rows, columns=["משפט", "פלט ידני", "פלט חזוי"])  # "Sentence", "Manual Output", "Predicted Output"

    # Write to Excel files (UTF-8-safe)
    correct_df.to_excel(correct_file, index=False)
    wrong_df.to_excel(wrong_file, index=False)
    print((caught / fours_and_fives)*100)
    print(fours_and_fives)
    print(caught)
    print(ones)
    print(wrongsT)


# def main():
#     if len(sys.argv) < 5:
#         print(
#             "Usage: python test_filter.py manual_outputs.txt "
#             "sentences.txt subjects.txt keywords.txt")
#         sys.exit(1)
#
#     manual_outputs_file = sys.argv[1]
#     sentences_file = sys.argv[2]
#     subjects_file = sys.argv[3]
#     keywords_file = sys.argv[4]
#     temp_output_file = "temp_output.txt"
#
#     sys.argv = ["filter.py", subjects_file, keywords_file, sentences_file,
#                 temp_output_file]
#     filter_main()
#
#     manual_outputs = load_manual_outputs(manual_outputs_file)
#     predicted_outputs = load_predicted_outputs(temp_output_file)
#
#     evaluate_accuracy(manual_outputs, predicted_outputs)


def main():
    if len(sys.argv) < 5:
        print(
            "Usage: python test_filter.py manual_outputs.txt "
            "sentences.txt subjects.txt keywords.txt")
        sys.exit(1)

    manual_outputs_file = sys.argv[1]
    sentences_file = sys.argv[2]
    subjects_file = sys.argv[3]
    temp_output_file = "temp_output.txt"
    sys.argv = ["GPTfilter.py",sentences_file, subjects_file]
    # GPTmain()

    # Load and evaluate
    manual_outputs = load_manual_outputs(manual_outputs_file)
    predicted_outputs = load_predicted_outputs(temp_output_file)
   # evaluate_accuracy(manual_outputs, predicted_outputs)
    divide_to_files(manual_outputs, predicted_outputs, sentences_file)


if __name__ == "__main__":
    main()



#1324-1339 err, i put 1