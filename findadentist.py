# -*- coding: utf-8 -*-
#==============================================================================
#title           :findadentist.py
#description     :Extract Dentist's profiles from the findadentist.ada.org website.
#author          :Patrick Alves (cpatrickalves@gmail.com)
#date            :29-03-2019
#usage           :python findadentist.py inputfile.json
#output          :Another JSON file (output.json) with dentist's data
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

# Creating the header to allow requestings to the findadentist.ada.org API
headers = { "Authorization": "Basic NUNtQitIcVZuOXhTVnFKNkhiZC8xSGZnb29NdU1ZaXk=",            
            "Referer": "https://findadentist.ada.org/search-results?specialty=1&address=90014&distance=100&searchResultsReferrer=true",
          }

# Dentist's specialty code mapping
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
       
    # Check if the response was received
    if response.status_code != 200:
        logger.warn("You got blocked, change your IP address and try again")
        sys.exit()

    # Wait some time to avoid blocking
    wait_time = 20
    logger.info("Waiting {} seconds to avoid blocking ...".format(wait_time))
    sleep(wait_time)
    
    # Saves the Address Ids 
    data = json.loads(response.text)
    for dentist in data['Dentists']:
        dentists_address_ids.append(dentist['AddressId'])

logger.info("{} dentists obtained".format(len(dentists_address_ids)))

# Checking if there id any repeated ID
repeated_ids = len(dentists_address_ids) - len(list(set(dentists_address_ids)))
if repeated_ids != 0:
    # Removing repetead IDs
    dentists_address_ids = list(set(dentists_address_ids))
    logger.info("There are {} dentists repeated IDs".format(repeated_ids))

# Get the dentist's data from website API using the AddressIDs
dentists_counter = 1
dentists_data = [] # List object that saves the dentist's data
for dentist_id in dentists_address_ids:
    # Make request
    logger.info("Getting data for dentist ID {} - {}/{}".format(dentist_id, dentists_counter, len(dentists_address_ids)))
    dentists_counter += 1
    response = requests.get("https://findadentist.ada.org/api/DentistProfile?AddressId={}".format(dentist_id), headers=headers)
           
    # Check if the response was received
    if response.status_code != 200:
        logger.warn("You got blocked, change your IP address and try again")
        sys.exit()
    
    # Wait some time to avoid blocking
    wait_time = 20
    logger.info("Waiting {} seconds to avoid blocking ...".format(wait_time))
    sleep(wait_time)
    
    # Saving dentist's data
    data = json.loads(response.text)
    # Put the data in JSON schema
    formated_data = {
                    "Dentist Name": data["Name"],
                    "Specialty": data["Specialty"],
                    "ProfieImage_URL": data["Photo"],
                    "website": data["WebSite"],
                    "language": data["Languages"],
                    "Education": data["Education"][0]["Name"],
                    "Gender": data["Gender"],
                    "Payment Options": data["PaymentOptions"],
                    
                    "Contact Info": 
                    {
                    "Phone": data["Phone"],
                    "Address": data["Address"],
                    "City": data["City"],
                    "State": data["State"],
                    "Zip": data["Zip"]
                    },
                    "Proximity": 
                    {
                    "Distance": "???",
                    "InputZip": "???"
                    }
                }

    # Saving the data in the list
    dentists_data.append(formated_data)

# Saving the data in a JSON file
output_data = {"FindDentist_Output": dentists_data}
output_filename = 'output.json'
logger.info("Saving the data in {} file".format(output_filename))
with open(output_filename, 'w', encoding='utf-8') as outfile:
    json.dump(output_data, outfile, indent=4)



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

PENDENCIAS
- Checar schema
- Checar Ingles dos comentários
- Criar o container

"""