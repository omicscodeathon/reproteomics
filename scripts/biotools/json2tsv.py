# Import necessary libraries
import pandas as pd  # Used for handling data in DataFrame format and exporting to CSV/TSV
import json  # Used for working with JSON data
import argparse  # Used for creating command-line interfaces
import logging  # Used for logging messages, useful for debugging and tracking script progress
from pathlib import Path  # Used for handling file paths in a more reliable way

# Set up logging to track what's happening in the script
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to clean text data by removing newlines
def clean_text(text):
    # Check if the input is a string
    if isinstance(text, str):
        return text.replace('\n', ' ')  # Replace newline characters with spaces
    return text  # If it's not a string, return it as is

# Function to clean a list by joining elements into a string
def clean_list(lst):
    # Check if the input is a list
    if isinstance(lst, list):
        # Join list items into a string, converting dictionaries to JSON strings if needed
        return ', '.join([json.dumps(item) if isinstance(item, dict) else str(item) for item in lst])
    return lst  # If it's not a list, return it as is

# Function to extract publication details from the 'Publications' field
def extract_publications(publications):
    # Check if 'Publications' is a list (common in JSON data)
    if isinstance(publications, list):
        extracted_data = []
        # Loop through each publication entry in the list
        for pub in publications:
            if isinstance(pub, dict):  # Ensure each entry is a dictionary
                doi = pub.get('doi', '')  # Extract DOI, default to empty string if not present
                title = pub.get('metadata', {}).get('title', '') if isinstance(pub.get('metadata'), dict) else ''
                abstract = pub.get('metadata', {}).get('abstract', '').replace('\n', ' ') if isinstance(pub.get('metadata'), dict) else ''
                extracted_data.append({
                    'DOI': doi,
                    'Title': title,
                    'Abstract': abstract
                })
        return extracted_data
    
    # If 'Publications' is a string, try to split it into DOI, Title, Abstract
    elif isinstance(publications, str) and publications.strip():
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
    
    return []  # Return an empty list if 'Publications' is not in a recognized format

# Function to process each entry in the JSON data
def process_entry(entry):
    processed_entry = {}
    # Loop through each key-value pair in the entry
    for key, value in entry.items():
        if key != 'Publications':  # Skip 'Publications' for now, we'll handle it separately
            processed_entry[key] = clean_list(value) if isinstance(value, list) else clean_text(value)
    
    # Extract publications data from the 'Publications' field
    publications_data = extract_publications(entry.get('Publications', ''))
    return processed_entry, publications_data

# Main function to convert JSON data to a DataFrame and save it as a TSV file
def json_to_dataframe(json_file, tsv_file):
    try:
        # Try to open and load the JSON file
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

    # Loop through each entry in the JSON data
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
        result_df = pd.DataFrame(publications_data)  # Create a DataFrame from the processed data
        logging.info(f"DataFrame head: \n{result_df.head()}")

        try:
            result_df.to_csv(tsv_file, sep='\t', index=False)  # Save the DataFrame as a TSV file
            logging.info(f"File saved successfully as {tsv_file}")
        except Exception as e:
            logging.error(f"Failed to save file: {e}")
    else:
        logging.warning("No data to save. The resulting file will be empty.")

# Arguments on Command-line interface (CLI) part
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
