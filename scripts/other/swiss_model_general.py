import requests
import time

# Replace with your SWISS-MODEL token
token = "MY_SWISS_MODEL_API_TOKEN"

# Function to perform homology modeling with user template
def perform_user_template_homology_modeling(target_sequences, template_coordinates):
    # Start a new job for user template homology modelling
    response = requests.post(
        "https://swissmodel.expasy.org/user_template",
        headers={ "Authorization": f"Token {token}" },
        json={
            "target_sequences": target_sequences,
            "template_coordinates": template_coordinates,
            "project_title": "Thalassemia"
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

# Example target sequences and template coordinates
target_sequences = [
    "AMINO_ACID_SEQUENCE"
]

# Load template coordinates from file
# Must have pdb file downloaded already
with open("sample.pdb") as f:
    template_coordinates = f.read()

# Perform user template homology modeling
perform_user_template_homology_modeling(target_sequences, template_coordinates)
