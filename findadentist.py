# -*- coding: utf-8 -*-
#==============================================================================
#title           :findadentist.py
#description     :Extract Dentist's profiles from the findadentist.ada.org website.
#author          :Patrick Alves (cpatrickalves@gmail.com)
#date            :29-03-2019
#usage           :python findadentist.py inputfile.json
#python_version  :3.6
#==============================================================================

import requests
import json
import sys
from time import sleep
from logzero import logger


logger.info('Starting findadentist.py script ...')

# Check if the input file was in the command parameters
if (len(sys.argv) < 2):
    logger.error("Missing input file! You need to pass the JSON input file as a script's parameter.")
    logger.error('<usage>: python findadentist.py inputfile.json')
    sys.exit()

# Load JSON file with input data
logger.info("Loading input file: {}".format(sys.argv[1]))
try:
    with open(sys.argv[1]) as json_file:  
        input_data = json.load(json_file)

except Exception as exc:
    logger.error(str(exc))
    sys.exit()

# Creating requestings to the API
headers = { "Authorization": "Basic NUNtQitIcVZuOXhTVnFKNkhiZC8xSGZnb29NdU1ZaXk=",            
            "Referer": "https://findadentist.ada.org/search-results?specialty=1&address=90014&distance=100&searchResultsReferrer=true",
          }

# Specialty code mapping
# All specialty are mapped to a code before request the data
specialty = {"General Practice": 1,
            "Oral and Maxillofacial Surgery": 2,
            "Endodontics": 3,
            "Orthodontics and Dentofacial Orthopedics": 4, 
            "Orthodontics": 4,
            "Pediatric Dentistry": 5,
            "Periodontics": 6,
            "Prosthodontics": 7,
            "Oral and Maxillofacial Pathology": 8,
            "Dental Public Health": 9,
            "Oral and Maxillofacial Radiology": 10
            }

# Loop through input data searchs for the dentists and saves each Dentist AddressId
dentists_address_ids = []
total_searchs = len(input_data['FindDentist_Input'])
searchs_counter = 1
for inputs in input_data['FindDentist_Input']:
    # Building URL
    url = 'https://findadentist.ada.org/api/Dentists?Address={}&Specialty={}&Distance={}'.format(inputs['zip code'], 
                                                                                                 specialty[inputs['specialty']], 
                                                                                                 inputs['distance'])
    # Make request
    logger.info("Performing search {}/{} - requested page: {}".format(searchs_counter, total_searchs, url))
    searchs_counter += 1
    response = requests.get(url, headers=headers)    

    # Wait some time to avoid blocking
    wait_time = 15
    logger.info("Waiting {} seconds to avoid blocking ...".format(wait_time))
    sleep(wait_time)
    
    # Check if the response was received
    if response.status_code != 200:
        logger.warn("You got blocked, change your IP address and try again")
        sys.exit()
    
    # Saves the Address Ids 
    data = json.loads(response.text)
    for dentist in data['Dentists']:
        dentists_address_ids.append(dentist['AddressId'])

logger.info("{} dentists obtained".format(len(dentists_address_ids)))


"""
Here is the website: https://findadentist.ada.org/

The requirements are:

Use the parameters from a JSON input file (provided)

zip code
distance
specialty

Use the parameters from the input JSON file to search for a list of dentists
Collect all the dentist name & contact info
If no results found, set the error status flag to “No result found”
Output a JSON file with all the dentist information and any error status

Output JSON must be validated against a pre-defined JSON schema

Deliverables

Share your code for review via your own GIT or Bitbucket account
Deliver a docker container that we can run your code

"""