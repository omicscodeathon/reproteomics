import requests
import time

# Replace with your SWISS-MODEL token
token = "MY_SWISS_MODEL_API_TOKEN"

# Function to perform homology modeling
def perform_homology_modeling(target_sequences, template_sequence):
    # Start a new job for homology modeling
    response = requests.post(
        "https://swissmodel.expasy.org/automodel",
        headers={ "Authorization": f"Token {token}" },
        json={ 
            "target_sequences": target_sequences,
            "project_title": "Homology Modeling Example"
        })

    # Check status code
    if response.status_code == 202:
        project_id = response.json()["project_id"]
        print(f"Job started with project ID: {project_id}")
    else:
        print("Error starting modeling job.")
        return

    # Polling loop for job status
    while True:
        time.sleep(10)

        response = requests.get(
            f"https://swissmodel.expasy.org/project/{project_id}/models/summary/", 
            headers={ "Authorization": f"Token {token}" })

        status = response.json()["status"]
        print(f"Job status is now {status}")

        if status in ["COMPLETED", "FAILED"]:
            break

    # Check if job is COMPLETED and fetch the model coordinates
    response_object = response.json()
    if response_object['status'] == 'COMPLETED':
        for model in response_object['models']:
            print("Model coordinates URL:", model['coordinates_url'])
    else:
        print("Modeling job failed.")

# Example target and template sequences
target_sequences = [
    "AMINI_ACID_SEQUENCE",
    "AMINO_ACID_SEQUENCE"
]
template_sequence = "AMINO_ACID_SEQUENCE"

# Perform homology modeling
perform_homology_modeling(target_sequences, template_sequence)
