# Optional: Setup logging
import logging  # Import logging module to handle and format log messages
import requests  # Import requests module for making HTTP requests
from requests.exceptions import RequestException  # Import exception for handling request errors
import json  # Import JSON module to handle JSON data
import argparse  # Import argparse module to handle command-line arguments

# Set up logging configuration
# This configuration will print log messages to the console with the format: timestamp - log level - message
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to extract topic terms from a list of dictionaries and join them into a single string
def extract_topics(topics):
    # Check if 'topics' is a list
    if isinstance(topics, list):
        # Iterate over the list and get the "term" key from each dictionary, join terms with a comma
        return ', '.join(topic.get("term", "") for topic in topics if isinstance(topic, dict))
    # If 'topics' is not a list, return it as is
    return topics

# Function to extract the first documentation URL from a list of documentation dictionaries
def extract_documentation(documentation):
    # Check if 'documentation' is a list
    if isinstance(documentation, list):
        # Iterate over the list to find the first dictionary and return the "url" key
        for doc in documentation:
            if isinstance(doc, dict):
                return doc.get("url", "")
    # If 'documentation' is not a list, return it as is
    return ""

# Function to extract and format publication details (DOI, title, abstract) from a list of publication dictionaries
def extract_publications(publications):
    # Check if 'publications' is a list
    if isinstance(publications, list):
        extracted = []  # Initialize an empty list to store formatted publication strings
        # Iterate over the list to extract and format the publication details
        for pub in publications:
            if isinstance(pub, dict):
                doi = pub.get("doi", "")  # Extract the DOI
                metadata = pub.get("metadata", {})  # Extract the metadata dictionary
                title = metadata.get("title", "") if isinstance(metadata, dict) else ""  # Extract the title
                abstract = metadata.get("abstract", "").replace('\n', ' ') if isinstance(metadata, dict) else ""  # Extract and format the abstract
                # Append the formatted string to the 'extracted' list
                extracted.append(f"{doi}, {title}, {abstract}")
        # Join the extracted publication strings with '; ' and return
        return '; '.join(extracted)
    # If 'publications' is not a list, return it as is
    return publications

# Function to safely join list elements into a string
def safe_join(lst):
    # Check if 'lst' is a list
    if isinstance(lst, list):
        # Convert each item to a string and join with a comma
        return ', '.join(str(item) for item in lst)
    # If 'lst' is not a list, convert it to a string and return
    return str(lst)

# Function to fetch tools from the bio.tools API based on a search query
def fetch_biotools(query):
    url = "https://bio.tools/api/tool/"  # Base URL of the bio.tools API
    params = {"q": query, "format": "json", "page_size": 100}  # Query parameters for the API request
    all_tools = []  # Initialize an empty list to store all tools
    page = 1  # Start with the first page of results

    while True:  # Loop to fetch all pages of results
        try:
            params["page"] = page  # Update the page number in the query parameters
            response = requests.get(url, params=params)  # Make the GET request to the API
            response.raise_for_status()  # Raise an error for bad HTTP responses (e.g., 404, 500)
        except RequestException as e:  # Handle any request errors
            logging.error(f"Error: Failed to fetch data for page {page}: {e}")
            break  # Exit the loop if there is an error

        data = response.json()  # Parse the JSON response
        tools_on_page = data.get("list", [])  # Get the list of tools on the current page

        if not tools_on_page:  # If no tools are found on this page, exit the loop
            break

        # Loop through each tool in the current page
        for tool in tools_on_page:
            # Extract and format the relevant information for each tool
            filtered_tool = {
                "Name": tool.get("name"),
                "Homepage": tool.get("homepage"),
                "Description": tool.get("description", "").replace('\n', ' '),
                "Version": tool.get("version"),
                "Tool Type": safe_join(tool.get("toolType", [])),
                "Topic": extract_topics(tool.get("topic")),
                "Publications": extract_publications(tool.get("publication")),
                "Operation": safe_join(tool.get("operation", [])),
                "Input": safe_join(tool.get("input", [])),
                "Output": safe_join(tool.get("output", [])),
                "Documentation": extract_documentation(tool.get("documentation", [])),
                "Operating System": safe_join(tool.get("operatingSystem", [])),
                "Language": safe_join(tool.get("language", [])),
                "Accessibility": safe_join(tool.get("accessibility", "")),
                "License": safe_join(tool.get("license", []))
            }
            all_tools.append(filtered_tool)  # Add the formatted tool to the list

        page += 1  # Increment the page number to fetch the next page

    return all_tools  # Return the list of all fetched and formatted tools

# Function to save the fetched tools to a JSON file
def save_to_file(tools, filename):
    try:
        with open(filename, 'w') as f:  # Open the specified file in write mode
            json.dump(tools, f, indent=4)  # Write the tools list to the file as JSON, formatted with indentation
        logging.info(f"Data saved to {filename}")  # Log a success message
    except IOError as e:  # Handle any file write errors
        logging.error(f"Error: Could not write to file {filename}: {e}")

# Main function to parse command-line arguments and execute the script
def main():
    parser = argparse.ArgumentParser(description='Fetch tools from bio.tools.')  # Create an argument parser
    parser.add_argument('query', type=str, help='The search query string.')  # Add a positional argument for the search query
    parser.add_argument('output', type=str, help='The output JSON file.')  # Add a positional argument for the output file name
    args = parser.parse_args()  # Parse the command-line arguments

    biotools = fetch_biotools(args.query)  # Fetch the tools from bio.tools based on the query
    save_to_file(biotools, args.output)  # Save the fetched tools to the specified output file
    logging.info(f"Total {len(biotools)} tools fetched.")  # Log the number of tools fetched

# Entry point of the script; this block runs if the script is executed directly
if __name__ == "__main__":
    main()
