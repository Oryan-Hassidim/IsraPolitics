import csv
import os
import Utils.rank_to_client_data as r


output_dir = "Jobs/511/התיישבות"

csv_path = "Client/client_data/mk_data/511/התיישבות.csv"
with open(csv_path, "w", encoding="utf-8",newline='') as csv_file:
    writer = csv.writer(csv_file, quoting=csv.QUOTE_MINIMAL)
    writer.writerow(["Id", "Date", "Topic", "Text", "Rank"])
    # for each line in the filter output file, get the corresponding
    # text,id,rank, and extract date and topic from db
    rows = r.load_ranked_data_with_metadata(
        os.path.join(output_dir, "ids.txt"),
        os.path.join(output_dir, "texts.txt"),
        os.path.join(r.JOBS_DIR,"התיישבות", "filter_output.txt"),
        os.path.join(r.BASE_DIR,"Utils", "date_topic_per_sentence_id.sql")
    )
    for speech_id, date, topic, text, rank in rows:
        writer.writerow([speech_id, date, topic, text, rank])

