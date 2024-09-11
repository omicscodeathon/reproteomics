import pandas as pd
import json
import argparse
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def clean_text(text):
    if isinstance(text, str):
        return text.replace('\n', ' ')
    return text

def clean_list(lst):
    if isinstance(lst, list):
        return ', '.join([json.dumps(item) if isinstance(item, dict) else str(item) for item in lst])
    return lst

def extract_publications(publications):
    if isinstance(publications, list):
        extracted_data = []
        for pub in publications:
            if isinstance(pub, dict):
                doi = pub.get('doi', '')
                title = pub.get('metadata', {}).get('title', '') if isinstance(pub.get('metadata'), dict) else ''
                abstract = pub.get('metadata', {}).get('abstract', '').replace('\n', ' ') if isinstance(pub.get('metadata'), dict) else ''
                extracted_data.append({
                    'DOI': doi,
                    'Title': title,
                    'Abstract': abstract
                })
        return extracted_data
    
    elif isinstance(publications, str) and publications.strip():
        # If `Publications` is a string, attempt to split it into components
        parts = publications.split(', ')
        if len(parts) >= 3:
            doi = parts[0]
            title = parts[1]
            abstract = ', '.join(parts[2:]).replace('\n', ' ')
        else:
            doi = ''
            title = parts[0] if len(parts) > 0 else ''
            abstract = ', '.join(parts[1:]).replace('\n', ' ') if len(parts) > 1 else ''

        return [{
            'DOI': doi,
            'Title': title,
            'Abstract': abstract
        }]
    
    return []

def process_entry(entry):
    processed_entry = {}
    for key, value in entry.items():
        if key != 'Publications':  # Skip publications for now
            processed_entry[key] = clean_list(value) if isinstance(value, list) else clean_text(value)
    
    publications_data = extract_publications(entry.get('Publications', ''))
    return processed_entry, publications_data

    
    publications_data = extract_publications(entry.get('publications', []))
    return processed_entry, publications_data

def json_to_dataframe(json_file, tsv_file):
    try:
        with open(json_file, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        logging.error(f"File not found: {json_file}")
        return
    except json.JSONDecodeError:
        logging.error(f"Invalid JSON format: {json_file}")
        return

    processed_data = []
    publications_data = []

    for entry in data:
        logging.info(f"Processing entry: {entry}")
        processed_entry, pub_data = process_entry(entry)
        
        if pub_data:
            for pub in pub_data:
                merged_entry = {**processed_entry, **pub}
                publications_data.append(merged_entry)
        else:
            logging.warning(f"No publications found for entry: {processed_entry['Name']}")

    logging.info(f"Total processed data: {len(publications_data)} entries.")

    if publications_data:
        result_df = pd.DataFrame(publications_data)
        logging.info(f"DataFrame head: \n{result_df.head()}")

        try:
            result_df.to_csv(tsv_file, sep='\t', index=False)
            logging.info(f"File saved successfully as {tsv_file}")
        except Exception as e:
            logging.error(f"Failed to save file: {e}")
    else:
        logging.warning("No data to save. The resulting file will be empty.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert JSON data to TSV.')
    parser.add_argument('json_file', type=str, help='The input JSON file.')
    parser.add_argument('tsv_file', type=str, help='The output TSV file.')

    args = parser.parse_args()

    json_file = Path(args.json_file)
    tsv_file = Path(args.tsv_file)

    if not json_file.exists():
        logging.error(f"Input file does not exist: {json_file}")
    elif not tsv_file.parent.exists():
        logging.error(f"Output directory does not exist: {tsv_file.parent}")
    else:
        json_to_dataframe(json_file, tsv_file)
