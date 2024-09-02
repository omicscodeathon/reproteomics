import os
import requests

url = 'https://rest.uniprot.org/uniprotkb/stream?format=fasta&query=%28%28proteome%3AUP000005640%29%29'
response = requests.get(url)

if response.status_code == 200:
    fasta_data = response.text
    output_filename = 'HRP.fasta'
    output_file_path = os.path.join(os.getcwd(), output_filename)
    with open(output_file_path, 'w') as file:
        file.write(fasta_data)
    print("FASTA file saved as:", output_file_path)
else:
    print("Error occurred while retrieving the FASTA file:", response.status_code)
