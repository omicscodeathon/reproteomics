#load modules that will be used
import os
import requests
import logging

# Configure logging with a basic configuration (https://docs.python.org/3/howto/logging-cookbook.html)
#Logging messages which are less severe than level will be ignored
logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(levelname)s - %(message)s')

# Create a console handler and set its log level to INFO
#StreamHandler sends logging output to streams such as sys.stdout, sys.stderr or any file-like object
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Create a formatter and add it to the console handler
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

# Add the console handler to the root logger that is created
logging.getLogger('').addHandler(console_handler)

#Defines the function. Give function a specific name. Specify the files that will be used in the command.
def download_file(url, output_path):
    #Sends an HTTP get request to the provided url using the requests library. The response from the server is stored in the response variable
    response = requests.get(url)
    #Checks if the HTTP response status code is 200, which indicates a successful request. If the condition is true, it means the file was successfully retrieved from the server.
    if response.status_code == 200:
