import os
from typing import Generator


def apply_filter(filter_output_path: str, file_to_filter: str, output_path: str) -> bool:
    """
    Applies a filter to a text file based on scores from a GPT filter output.

    This function reads two files in parallel:
    - `filter_output_path`: contains integer scores (one per line).
    - `file_to_filter`: contains text lines corresponding to the same indices.

    For each pair of lines, if the score is 4 or higher, the corresponding line
    from `file_to_filter` is written to `output_path`.

    The function also checks for the existence of input and output files and
    creates the output directory if it does not exist.

    :param filter_output_path: Path to the file containing filter scores (one integer per line).
    :param file_to_filter: Path to the input text file to be filtered line by line.
    :param output_path: Path to the output file where accepted lines will be written.
    :return: None
    """

    # Check if the input file exists
    if not os.path.isfile(file_to_filter):
        print(f"Input file '{file_to_filter}' does not exist.")
        return False
    # Check if the filter output file exists
    if not os.path.isfile(filter_output_path):
        print(f"Filter output file '{filter_output_path}' does not exist.")
        return False
    # Check if the output file already exists
    if os.path.isfile(output_path):
        print(f"Output file '{output_path}' already exists. exitsing.")
        return False
    # Check if the output directory exists
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    

    with (
        open(filter_output_path, "r", encoding="utf-8") as filter_output_file,
        open(file_to_filter, "r", encoding="utf-8") as file_to_filter_file,
        open(output_path, "w", encoding="utf-8") as output_file,
    ):
        filter_output: Generator[int, None, None] = (
            int(line.strip()) for line in filter_output_file if line.strip()
        )
        file_to_filter_lines: Generator[str, None, None] = (
            line.strip() for line in file_to_filter_file if line.strip()
        )

        for filter_output_line, file_to_filter_line in zip(
            filter_output, file_to_filter_lines
        ):
            if filter_output_line >= 4:
                output_file.write(f"{file_to_filter_line}\n")
    return True

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 4:
        print("Usage: python filter.py filter_output.txt file_to_filter.txt output.txt")
        sys.exit(1)
    filter_output_path = sys.argv[1]
    file_to_filter = sys.argv[2]
    output_path = sys.argv[3]

    apply_filter(filter_output_path, file_to_filter, output_path)