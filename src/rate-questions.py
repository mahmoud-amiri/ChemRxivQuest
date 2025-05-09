# SPDX-License-Identifier: CC-BY-4.0

import json
import openai
import time
import os
import pandas as pd
import re

# Load OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Paths
input_csv_path = "updated_chunking_eval.csv"
output_json_path = "chemistry_extraction_validation.jsonl"
response_log_path = "openai_relevance_responses.jsonl"

# Function to clean OpenAI response
def clean_openai_response(response_text):
    """ Cleans OpenAI response by removing JSON formatting artifacts. """
    response_text = response_text.strip()
    response_text = re.sub(r"^```json\n?", "", response_text)  # Remove leading ```json
    response_text = re.sub(r"\n?```$", "", response_text)  # Remove trailing ```
    response_text = response_text.strip()
    return response_text  # Ensure only JSON content remains

# Function to safely parse JSON response
def safe_json_parse(json_text):
    """ Ensures the response is a valid JSON string before parsing. """
    try:
        print(f"[DEBUG] Parsing JSON: {repr(json_text)}")  # Show exact representation
        parsed_data = json.loads(json_text)  # Load JSON safely
        return parsed_data
    except json.JSONDecodeError as e:
        print(f"[ERROR] JSON Parsing Failed: {e}\nProblematic JSON: {repr(json_text)}")
        return None  # Return None if parsing fails

# Function to query OpenAI for relevance checking
def check_relevance(question, answer, retries=3, backoff_factor=2):
    """ Sends question and answer to OpenAI to check if the answer is relevant to the question. """

    prompt = f"""
    You are an AI assistant validating whether an extracted answer is related to a given question.

    **Question:** {question}

    **Extracted Answer:** {answer}

    **Task:**  
    Determine the relationship between the extracted answer and the question. Do not worry about completeness or minor wording differences.

    - `"Relevant"` → The answer is directly related to the question.
    - `"Somewhat Relevant"` → The answer has partial relevance but does not fully match.
    - `"Not Relevant"` → The answer is unrelated to the question.

    **Important:** Ignore minor extra text unless it completely changes the meaning.  
    Return only a valid JSON object like this:  
    {{"relevance": "Relevant"}}
    """

    for attempt in range(retries):
        try:
            response = openai.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are an AI extraction validator."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.0  # Reduce randomness
            )

            raw_response = response.choices[0].message.content.strip()

            # Clean OpenAI response
            cleaned_response = clean_openai_response(raw_response)

            print(f"[DEBUG] Cleaned OpenAI Response: {repr(cleaned_response)}")  # Show exact string for debugging

            # Log raw and cleaned responses in JSONL format
            with open(response_log_path, "a", encoding="utf-8") as f_log:
                log_data = {"question": question, "raw_response": raw_response, "cleaned_response": cleaned_response}
                f_log.write(json.dumps(log_data) + "\n")

            # Parse JSON safely
            parsed_response = safe_json_parse(cleaned_response)
            if parsed_response:
                return parsed_response  # Return parsed JSON if valid

        except (openai.OpenAIError, Exception) as e:
            print(f"[ERROR] Attempt {attempt + 1} failed: {e}")

            # Log errors
            with open(response_log_path, "a", encoding="utf-8") as f_log:
                f_log.write(json.dumps({"question": question, "error": str(e)}) + "\n")

            time.sleep(backoff_factor ** attempt)  # Exponential backoff

    return None  # Return None if all retries fail

# Function to process CSV and validate extracted answers
def process_csv():
    """ Reads CSV file, processes questions, and writes relevance validation results to JSONL. """

    df = pd.read_csv(input_csv_path)

    if "question" not in df.columns or "references" not in df.columns:
        print("[ERROR] CSV file is missing required columns: 'question' and 'references'")
        return

    processed_count = 0

    with open(output_json_path, "w", encoding="utf-8") as f_out:
        for index, row in df.iterrows():
            question = row["question"]
            answer = row["references"]

            print(f"\n[DEBUG] Processing Question {index+1}: {question}")

            result = check_relevance(question, answer)

            if result:
                output_data = {
                    "question": question,
                    "answer": answer,
                    "relevance": result.get("relevance", "Unknown")
                }

                f_out.write(json.dumps(output_data) + "\n")
                f_out.flush()

                processed_count += 1
                time.sleep(1)  # Prevent rate limits

    print(f"\n[INFO] Processing complete. {processed_count} questions analyzed.")

# Run script
if __name__ == "__main__":
    process_csv()
