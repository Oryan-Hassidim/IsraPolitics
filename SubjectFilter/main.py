def main():
    # usage: python subjectfilter.py system_prompt.txt input.txt
    # prints output to output-YYYY-MM-DD-HH-MM-SS.txt
    import os
    import sys
    from datetime import datetime

    if len(sys.argv) not in [3, 4]:
        print("Usage: python main.py system_prompt.txt input.txt [model]")
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

    # Optional parameter to choose model
    model = "gpt-4.1-mini"  # Default model
    if len(sys.argv) == 4:
        model = sys.argv[3]

    from gpt_jobs import send_job, start_batch_job, retrieve_batch_results

    # send_job(system_prompt_path, input_path, output_path, model)
    # id = start_batch_job(system_prompt_path, input_path, model)
    # print(id)
    id = "batch_68220927e07c81909797384f83c48d13"
    print(retrieve_batch_results(id, output_path))


if __name__ == "__main__":
    main()
