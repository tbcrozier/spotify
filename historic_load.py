import os
from google.cloud import bigquery
import json

def convert_array_json_to_ndjson(array_json_path, ndjson_output_path):
    """Converts an array-based JSON file to newline-delimited JSON (NDJSON)."""
    with open(array_json_path, 'r') as f:
        records = json.load(f)

    with open(ndjson_output_path, 'w') as f:
        for record in records:
            f.write(json.dumps(record) + '\n')


# 1. Initialize BigQuery client
client = bigquery.Client()

# 2. Set your variables
project_id = "vocal-spirit-372618"
dataset_id = "spotify"
table_id = "streaming_history"
directory_path = "/Users/ioa6870/repos/tbcrozier/spotify/data/historic/Spotify Extended Streaming History"
table_ref = f"{project_id}.{dataset_id}.{table_id}"

# 3. Configure the load job
job_config = bigquery.LoadJobConfig(
    source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
    autodetect=True,
    write_disposition=bigquery.WriteDisposition.WRITE_APPEND,  # Append each file to the table
)

# 4. Read and load all JSON files
for filename in os.listdir(directory_path):
    if filename.endswith(".json"):
        file_path = os.path.join(directory_path, filename)

        # Create temp NDJSON file
        temp_file_path = file_path.replace(".json", ".ndjson")
        print(f"Converting {file_path} -> {temp_file_path}")

        convert_array_json_to_ndjson(file_path, temp_file_path)

        # Load the temp NDJSON file
        with open(temp_file_path, "rb") as source_file:
            load_job = client.load_table_from_file(
                source_file,
                table_ref,
                job_config=job_config,
            )

        load_job.result()
        print(f"Loaded {load_job.output_rows} rows from {filename} into {table_ref}")

print("\n✅ All files loaded successfully!")

