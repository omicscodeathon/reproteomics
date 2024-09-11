##########################################################
## For a given list of proteins the script resolves them
## (if possible) to the best matching STRING identifier
## and prints out the mapping on screen in the TSV format
##
## Requires requests module:
## type "python -m pip install requests" in command line
## (win) or terminal (mac/linux) to install the module
###########################################################

import requests

def resolve_protein_identifiers(protein_list):
    string_api_url = "https://version-11-5.string-db.org/api"
    output_format = "tsv-no-header"
    method = "get_string_ids"

## Set parameters for API request
    params = {
        "identifiers": "\r\n".join(protein_list),
        "species": 9606,
        "limit": 1,
        "echo_query": 1,
    }

## Construct the API request URL
    request_url = "/".join([string_api_url, output_format, method])

## Send the API request and get the results
    results = requests.post(request_url, data=params)

## Parse the results and create a mapping
    protein_mapping = {}
    for line in results.text.strip().split("\n"):
        input_identifier, _, string_identifier, _ = line.split("\t")
        protein_mapping[input_identifier] = string_identifier

    return protein_mapping

def main():
    protein_list = ["P1", "P2", "P3", "P4"]  # Your protein list
    mapping = resolve_protein_identifiers(protein_list)

   # Print the mapping
    for input_id, string_id in mapping.items():
        print("Input:", input_id, "STRING:", string_id)
      
#ensures that the script's main functionality is only executed when the script is run directly
if __name__ == "__main__":
    main()

