import os
from typing import Generator


def filter(filter_output_path: str, file_to_filter: str, output_path: str) -> None:
    """ """

    # Check if the input file exists
    if not os.path.isfile(file_to_filter):
        print(f"Input file '{file_to_filter}' does not exist.")
        return
    # Check if the filter output file exists
    if not os.path.isfile(filter_output_path):
        print(f"Filter output file '{filter_output_path}' does not exist.")
        return
    # Check if the output file already exists
    if os.path.isfile(output_path):
        print(f"Output file '{output_path}' already exists. exitsing.")
        return
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

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 4:
        print("Usage: python filter.py filter_output.txt file_to_filter.txt output.txt")
        sys.exit(1)
    filter_output_path = sys.argv[1]
    file_to_filter = sys.argv[2]
    output_path = sys.argv[3]

    filter(filter_output_path, file_to_filter, output_path)