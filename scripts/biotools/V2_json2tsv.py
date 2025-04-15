import pandas as pd
import json
import argparse
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def clean_text(text):
    """Remove newlines and unnecessary spaces from text fields."""
    return text.replace("\n", " ") if isinstance(text, str) else text

def clean_list(lst):
    """Convert lists to a comma-separated string."""
    if isinstance(lst, list):
        return ", ".join(str(item) for item in lst)
    return str(lst)

def extract_publications(publications):
    """Extract relevant details from the Publications field."""
    extracted_data = []
    
    if isinstance(publications, list):
        for pub in publications:
            if isinstance(pub, dict):
                extracted_data.append({
                    "DOI": pub.get("doi", ""),
                    "Title": clean_text(pub.get("title", "")),
                    "Abstract": clean_text(pub.get("abstract", "")),
                    "Date": pub.get("date", ""),  
                    "Citation": pub.get("citation_count", 0),
                })
    return extracted_data

def process_entry(entry):
    """Extracts all fields, handling publications separately."""
    processed_entry = {
        key: clean_list(value) if isinstance(value, list) else clean_text(value)
        for key, value in entry.items() if key != "Publications"
    }
    
    publications_data = extract_publications(entry.get("Publications", []))
    
    # If no publications exist, return the entry as-is (to avoid losing tools without publications)
    if not publications_data:
        return [processed_entry]

    # If publications exist, merge tool details with each publication
    merged_entries = [{**processed_entry, **pub} for pub in publications_data]
    
    return merged_entries

def json_to_dataframe(json_file, tsv_file):
    """Reads JSON file, processes data, and saves it as a TSV file."""
    try:
        with open(json_file, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        logging.error(f"File not found: {json_file}")
        return
    except json.JSONDecodeError:
        logging.error(f"Invalid JSON format: {json_file}")
        return

    publications_data = []

    for entry in data:
        tool_name = entry.get("Name", "Unknown")
        logging.info(f"Processing entry: {tool_name}")
        
        processed_entries = process_entry(entry)
        publications_data.extend(processed_entries)

    logging.info(f"Total processed entries: {len(publications_data)}.")

    if publications_data:
        df = pd.DataFrame(publications_data)
        logging.info(f"DataFrame preview: \n{df.head()}")

        try:
            df.to_csv(tsv_file, sep="\t", index=False)
            logging.info(f"File saved successfully: {tsv_file}")
        except Exception as e:
            logging.error(f"Failed to save file: {e}")
    else:
        logging.warning("No data to save. The resulting file will be empty.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert JSON data to TSV.")
    parser.add_argument("json_file", type=str, help="The input JSON file.")
    parser.add_argument("tsv_file", type=str, help="The output TSV file.")

    args = parser.parse_args()

    json_file = Path(args.json_file)
    tsv_file = Path(args.tsv_file)

    if not json_file.exists():
        logging.error(f"Input file does not exist: {json_file}")
    elif not tsv_file.parent.exists():
        logging.error(f"Output directory does not exist: {tsv_file.parent}")
    else:
        json_to_dataframe(json_file, tsv_file)
