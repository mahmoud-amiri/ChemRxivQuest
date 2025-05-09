# SPDX-License-Identifier: CC-BY-4.0

import pandas as pd
import json
import os
import re
import signal
from fuzzysearch import find_near_matches
from rapidfuzz import fuzz, process

# ============ 🔧 TUNABLE PARAMETERS ============
FUZZY_MAX_L_DIST = 4  # More strict fuzzy matching to avoid incorrect matches
RAPIDFUZZ_THRESHOLD = 88  # Higher accuracy threshold to reduce mismatches
SLIDING_WINDOW_SIZE = 400  # Optimized for better context capture
SLIDING_WINDOW_STEP = 100  # Ensures overlapping search
TIMEOUT_SECONDS = 15  # Limits per-snippet search time
BUFFER = 10  # Fixes minor index mismatches
SIMILARITY_THRESHOLD = 80  # Don't flag mismatches if similarity is above this

# ============ 📂 FILE PATHS ============
TEXT_FOLDER = "./../full-text"
QUESTION_CSV = "./../hf/query.csv"
EXCERPT_CSV = "./../hf/snippet.csv"
OUTPUT_CSV = "chunking-eval-query-snippet.csv"
BACKUP_CSV = "chunking-eval-query-snippet-backup.csv"

# Load CSV files
questions_df = pd.read_csv(QUESTION_CSV)
excerpts_df = pd.read_csv(EXCERPT_CSV)

# ============ 🔄 TEXT NORMALIZATION ============
def normalize_text(text):
    """Lowercase, remove extra spaces, and normalize formatting."""
    if text is None:
        return ""
    text = text.lower().strip()
    text = re.sub(r'[“”]', '"', text)
    text = re.sub(r"[‘’]", "'", text)
    text = re.sub(r'\s+', ' ', text)  # Normalize spaces
    return text

# ============ 🔍 RAPIDFUZZ SEARCH ============
def find_best_match_rapidfuzz(snippet, full_text):
    """Finds the closest match using RapidFuzz with a sliding window."""
    snippet = normalize_text(snippet)
    full_text = normalize_text(full_text)

    best_match = None
    best_score = 0
    best_start = None

    for i in range(0, max(len(full_text) - SLIDING_WINDOW_SIZE, 1), SLIDING_WINDOW_STEP):
        chunk = full_text[i : i + SLIDING_WINDOW_SIZE]
        score = fuzz.partial_ratio(snippet, chunk)

        if score > best_score and score >= RAPIDFUZZ_THRESHOLD:
            best_score = score
            best_match = chunk
            best_start = i

    if best_match:
        return best_start, best_start + len(best_match)
    
    return None, None

# ============ ⏳ TIMEOUT HANDLER ============
def timeout_handler(signum, frame):
    raise TimeoutError("Snippet search took too long")

signal.signal(signal.SIGALRM, timeout_handler)

# Backup the existing CSV file if it exists
if os.path.exists(OUTPUT_CSV):
    os.rename(OUTPUT_CSV, BACKUP_CSV)
    print(f"📂 Backup created: {BACKUP_CSV}")

# ============ 🔍 MAIN PROCESS ============
results = []

for doc_id, group in excerpts_df.groupby("doc_id"):
    text_file = os.path.join(TEXT_FOLDER, f"{doc_id}.txt")

    if not os.path.exists(text_file):
        print(f"⚠️ Warning: {text_file} not found, skipping...")
        continue

    with open(text_file, "r", encoding="utf-8") as f:
        full_text = f.read()

    full_text_normalized = normalize_text(full_text)

    print(f"🔄 Processing doc_id={doc_id}, total snippets={len(group)}")

    for _, row in group.iterrows():
        snippet = row["text_snippet"]
        snippet_normalized = normalize_text(snippet)

        question_row = questions_df[(questions_df["doc_id"] == doc_id) & (questions_df["id"] == row["id"])]
        if question_row.empty:
            print(f"⚠️ No question found for doc_id={doc_id}, id={row['id']}")
            continue

        question = question_row.iloc[0]["question"]

        signal.alarm(TIMEOUT_SECONDS)  # Set timeout

        try:
            # First, try exact substring search
            start_idx = full_text.find(snippet)

            if start_idx != -1:
                end_idx = start_idx + len(snippet)
            else:
                # Fuzzy search if exact match fails
                matches = find_near_matches(snippet_normalized, full_text_normalized, max_l_dist=FUZZY_MAX_L_DIST)

                if matches:
                    best_match = matches[0]
                    start_idx, end_idx = best_match.start, best_match.end
                else:
                    # RapidFuzz fallback
                    start_idx, end_idx = find_best_match_rapidfuzz(snippet, full_text)

            # Ensure indices are within bounds
            if start_idx is not None:
                start_idx = max(0, start_idx - BUFFER)
                end_idx = min(len(full_text), end_idx + BUFFER)

                # Verify extracted snippet for similarity check
                extracted_snippet = full_text[start_idx:end_idx]
                similarity = fuzz.ratio(normalize_text(snippet), normalize_text(extracted_snippet))

                # Ignore mismatches if similarity is above threshold
                if similarity < SIMILARITY_THRESHOLD:
                    print(f"   ❌ Low similarity ({similarity}%) - Possible mismatch")
                    start_idx, end_idx = None, None
            else:
                print(f"   ❌ No match found")

        except TimeoutError:
            print(f"   ⏳ Timeout reached, skipping snippet")
            start_idx, end_idx = None, None

        # Append results
        reference = {"content": snippet, "start_index": start_idx, "end_index": end_idx}
        results.append([question, json.dumps([reference]), f"data/{doc_id}.txt"])

output_df = pd.DataFrame(results, columns=["question", "references", "corpus_id"])
output_df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8")

print(f"✅ Database saved to {OUTPUT_CSV}")
