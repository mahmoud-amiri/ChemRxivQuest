# SPDX-License-Identifier: CC-BY-4.0

import json

# File paths
output_json_path = "./../hf/extracted_metadata.jsonl"  # Output JSONL file
total_entries = 156  # Expected number of entries

def find_missing_doc_ids():
    """Checks for missing doc_ids in the output JSONL file."""
    expected_doc_ids = set(range(total_entries))  # Expected doc_id range
    processed_doc_ids = set()

    # Read the output file and extract processed doc_ids
    with open(output_json_path, "r", encoding="utf-8") as f:
        for line in f:
            try:
                record = json.loads(line.strip())  # Parse JSON
                if "doc_id" in record:
                    processed_doc_ids.add(record["doc_id"])
            except json.JSONDecodeError as e:
                print(f"[ERROR] Skipping invalid JSON line: {e}")

    # Find missing doc_ids
    missing_doc_ids = expected_doc_ids - processed_doc_ids

    if missing_doc_ids:
        print("\n🚨 Missing doc_ids:", sorted(missing_doc_ids))
    else:
        print("\n✅ All doc_ids are present!")

# Run the checker
find_missing_doc_ids()
