import requests
import json
import argparse
import logging
from requests.exceptions import RequestException

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to extract topic terms (remove URI) and concatenate them into a single string
def extract_topics(topics):
    if isinstance(topics, list):
        return ', '.join(topic.get("term", "") for topic in topics if isinstance(topic, dict))
    return topics

# Function to extract documentation URL
def extract_documentation(documentation):
    if isinstance(documentation, list):
        for doc in documentation:
            if isinstance(doc, dict):
                return doc.get("url", "")
    return ""

# Function to extract publication details (DOI, title, and abstract) and format them
def extract_publications(publications):
    if isinstance(publications, list):
        extracted = []
        for pub in publications:
            if isinstance(pub, dict):
                doi = pub.get("doi", "")
                metadata = pub.get("metadata", {})
                title = metadata.get("title", "") if isinstance(metadata, dict) else ""
                abstract = metadata.get("abstract", "").replace('\n', ' ') if isinstance(metadata, dict) else ""
                extracted.append(f"{doi}, {title}, {abstract}")
        return '; '.join(extracted)
    return publications

# Function to join list elements into a string, handling cases where the input is not a list
def safe_join(lst):
    if isinstance(lst, list):
        return ', '.join(str(item) for item in lst)
    return str(lst)

# Function to fetch biotools tools based on a query
def fetch_biotools(query):
    url = "https://bio.tools/api/tool/"
    params = {"q": query, "format": "json", "page_size": 150}
    all_tools = []
    page = 1

    while True:
        try:
            params["page"] = page
            response = requests.get(url, params=params)
            response.raise_for_status()  # Raise HTTPError for bad responses
        except RequestException as e:
            logging.error(f"Error: Failed to fetch data for page {page}: {e}")
            break

        data = response.json()
        tools_on_page = data.get("list", [])

        if not tools_on_page:
            break

        for tool in tools_on_page:
            filtered_tool = {
                "Name": tool.get("name"),
                "Homepage": tool.get("homepage"),
                "Description": tool.get("description", "").replace('\n', ' '),
                "Version": tool.get("version"),
                "Tool Type": safe_join(tool.get("toolType", [])),
                "Topic": extract_topics(tool.get("topic")),
                "Publications": extract_publications(tool.get("publication")),
                "Documentation": extract_documentation(tool.get("documentation", [])),
                "Operating System": safe_join(tool.get("operatingSystem", [])),
                "Language": safe_join(tool.get("language", [])),
                "Accessibility": safe_join(tool.get("accessibility", "")),
                "License": safe_join(tool.get("license", []))
            }
            all_tools.append(filtered_tool)

        page += 1

    return all_tools

# Function to save the fetched tools to a JSON file
def save_to_file(tools, filename):
    try:
        with open(filename, 'w') as f:
            json.dump(tools, f, indent=4)
        logging.info(f"Data saved to {filename}")
    except IOError as e:
        logging.error(f"Error: Could not write to file {filename}: {e}")

# Main function to parse arguments and execute the script
def main():
    parser = argparse.ArgumentParser(description='Fetch tools from bio.tools.')
    parser.add_argument('query', type=str, help='The search query string.')
    parser.add_argument('output', type=str, help='The output JSON file.')
    args = parser.parse_args()

    biotools = fetch_biotools(args.query)
    save_to_file(biotools, args.output)
    logging.info(f"Total {len(biotools)} tools fetched.")

if __name__ == "__main__":
    main()
