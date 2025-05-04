
def main():
    # usage: python subjectfilter.py system_prompt.txt input.txt
    # prints output to output-YYYY-MM-DD-HH-MM-SS.txt
    import sys
    from datetime import datetime
    from oryan_gpt_filter import filter, create_filter_batch, get_batch_results
    import os
    
    if len(sys.argv) != 3:
        print("Usage: python subjectfilter.py system_prompt.txt input.txt")
        sys.exit(1)
    system_prompt_path = sys.argv[1]
    input_path = sys.argv[2]
    output_path = f"outputs/output-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.txt"
    # Check if the input file exists
    if not os.path.isfile(input_path):
        print(f"Input file '{input_path}' does not exist.")
        sys.exit(1)
    # Check if the system prompt file exists
    if not os.path.isfile(system_prompt_path):
        print(f"System prompt file '{system_prompt_path}' does not exist.")
        sys.exit(1)
    # Check if the output file already exists
    if os.path.isfile(output_path):
        print(f"Output file '{output_path}' already exists. Deleting it.")
        os.remove(output_path)
    # Check if the output directory exists
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # filter(system_prompt_path, input_path, output_path)
    # id = create_filter_batch(system_prompt_path, input_path)
    # print(id)
    id = 'batch_6817ae857bc881909f441f3b8093af70'
    print(get_batch_results(id, output_path))

    # print(f"Output written to '{output_path}' successfully.")


if __name__ == "__main__":
    main()
