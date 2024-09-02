#!/usr/bin/env python3

################################################################
## For each protein in a list, save the PNG image of
## STRING network of its 15 most confident interaction partners.
##
## Requires requests module:
## Install using "python -m pip install requests"
################################################################

import requests
import time

# Set STRING API URL and parameters
string_api_url = "https://version-11-5.string-db.org/api"
output_format = "image"
method = "network"
species_id = 9606  # Species NCBI identifier (Homo sapients)

# List of genes for which to fetch interaction networks
my_genes = [
    "G1", "G2",
    "G3", "G4"
]

# Construct base URL
base_url = "/".join([string_api_url, output_format, method])

# Loop through genes
for gene in my_genes:
    try:
        # Set parameters for the API request
        params = {
            "identifiers": gene,
            "species": species_id,
            "add_white_nodes": 15,
            "network_flavor": "confidence"
        }

        # Make the API request
        response = requests.post(base_url, data=params)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Save the network to a file
        file_name = f"{gene}_network.png"
        with open(file_name, 'wb') as fh:
            fh.write(response.content)

        print(f"Saved interaction network to {file_name}")

        # Sleep for a short duration to avoid overloading the server
        time.sleep(1)

    except requests.exceptions.RequestException as e:
        print(f"Error processing {gene}: {e}")
