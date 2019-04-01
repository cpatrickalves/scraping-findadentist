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
from random import randint

### Script parameters
# If set to True all requests will be made using a proxy server
use_proxy = True
# Default number of seconds to wait between requests
wait_time = 3                                           

# Function that makes the requests to the findadentist.ada.org API
def make_request(url):

    # Creating the header to allow requests to the findadentist.ada.org API
    headers = { "Authorization": "Basic NUNtQitIcVZuOXhTVnFKNkhiZC8xSGZnb29NdU1ZaXk=",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
                "Referer": "https://findadentist.ada.org/search-results?specialty=1&address=90014&distance=100&searchResultsReferrer=true",
              }  

    # Number of times the script will retry a request after a blocking
    request_retries_limit = 10 
    # Retries counter                                
    request_retries_counter = 0

    # Setup a proxy server
    if use_proxy:
        proxies = {'http': 'http://proxy.proxycrawl.com:9000',
                   'https': 'http://proxy.proxycrawl.com:9000'}      

        # Keep trying requests until the requests retries limit is reached
        while (True): 
            
            try:
                # Make request with proxy
                response = requests.get(url, headers=headers, proxies=proxies)                                  
                # If got the reponse stops the loop
                break

            # If got a error
            except:
                # Starts a random wait time and try the request again
                request_retries_counter += 1
                # Create a random timer based on the number of retries made 
                proxy_wait_time = wait_time * request_retries_counter
                logger.warn("Proxy connection error ... trying again in {} seconds ...".format(proxy_wait_time))                
                sleep(proxy_wait_time)   
                logger.warn("Trying a new request: {}".format(url))
            
            # Check if the number of retries was reached
            if request_retries_counter >= request_retries_limit:
                logger.error("Retries limit reached - Can't connect to the proxy server: {}".format(proxies['http']))
                logger.error("Closing the script.")
                sys.exit()
                 
    else:            
        # Make request with no Proxy
        response = requests.get(url, headers=headers, proxies=proxies)    
        
        # Check if the response was received
        # Status code 200 means that the response was successfully received
        # Status code 404 means that No results were found or that you get blocked
        
        # SEARCH PROFILE requests
        # If you get blocked the reponse status code is 404 and the text in the
        # response is '"Not Found"'

        # DENTIST PROFILE requests
        # The reponse for the Dentist Profile API always got the 200 status code, but
        # if you get blocked it responses with a JSON with null values .
        # Get the Person ID of the JSON in the response
        # If was a request to the Dentist profiles:
        dentist_profile_id_response = 1
        if 'DentistProfile' in url:
            dentist_profile_id_response = json.loads(response.text)['PersonId']

        while (dentist_profile_id_response == 0) or (response.text == '"Not found"'): 
            # Starts a random wait time and try the request again
            request_retries_counter += 1
            # Create a random timer based on the number of retries made
            random_wait_time = randint(20, 40) * request_retries_counter
            logger.warn("You got an unexpected response, you may have been blocked!")
            logger.warn("Waiting a random time: {} seconds ...".format(random_wait_time))
            sleep(random_wait_time)   
            logger.warn("Trying a new request: {}".format(url))
            response = requests.get(url, headers=headers, proxies=proxies)    

            # Check if the number of retries was reached
            if request_retries_counter >= request_retries_limit:
                logger.error("Retries limit reached - You may have been blocked, change your IP address and try again")
                logger.error("Closing the script.")
                sys.exit()

    return response


logger.info('Starting findadentist.py script ...')
if use_proxy: logger.debug("Using proxy server: proxy.proxycrawl.com:9000")

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

# Useful Variables
dentists_address_ids = []                               # Saves the dentists Ids
total_searchs = len(input_data['FindDentist_Input'])    # Number of searchs to be performed
searchs_counter = 1                                     

# Loop through input data searchs for the dentists and saves each Dentist AddressId
for inputs in input_data['FindDentist_Input']:
    
    # Building URL
    url = 'https://findadentist.ada.org/api/Dentists?Address={}&Specialty={}&Distance={}'.format(inputs['zip code'], 
                                                                                                 specialty[inputs['specialty']], 
                                                                                                 inputs['distance'])
    # Make the search request
    logger.info("Performing search {}/{} - requested page: {}".format(searchs_counter, total_searchs, url))
    searchs_counter += 1
    response = make_request(url)
    
    # Load the data in a dict object
    data = json.loads(response.text)
    
    # If no results found, show the message: “No result found”
    if 'Dentists' not in data.keys():
        logger.warn("No results found for the parameters: Address={}  Specialty={}  Distance={}".format(inputs['zip code'], 
                                                                                                 specialty[inputs['specialty']], 
                                                                                                 inputs['distance']))
        ## Wait some time to avoid blocking    
        #logger.debug("Waiting {} seconds to avoid blocking ...\n".format(wait_time))
        sleep(wait_time)   
        continue
    
    logger.info("{} dentists found.".format(len(data["Dentists"])))

    # Wait some time to avoid blocking    
    #logger.debug("Waiting {} seconds to avoid blocking ...\n".format(wait_time))
    sleep(wait_time)
   
    # Saves the Address Ids 
    for dentist in data["Dentists"]:
        dentists_address_ids.append(dentist["AddressId"])

logger.info("{} dentists IDs obtained\n".format(len(dentists_address_ids)))

# Checking if there id any repeated ID
repeated_ids = len(dentists_address_ids) - len(list(set(dentists_address_ids)))
if repeated_ids != 0:
    # Removing repetead IDs
    dentists_address_ids = list(set(dentists_address_ids))
    logger.warn("There are {} dentists repeated IDs".format(repeated_ids))
    logger.warn("Removing repeated IDs")

# Get the dentist's data from website API using the AddressIDs
dentists_counter = 1
dentists_data = [] # List object that saves the dentist's data

# Scraping data for each dentist ID
logger.info("Getting data for {} dentists".format(len(dentists_address_ids)))
for dentist_id in dentists_address_ids:
    # Make request
    logger.info("Getting data for dentist ID {} - {}/{}".format(dentist_id, dentists_counter, len(dentists_address_ids)))
    dentists_counter += 1
    url = "https://findadentist.ada.org/api/DentistProfile?AddressId={}".format(dentist_id)
    response = make_request(url)
    
    # Wait some time to avoid blocking    
    #logger.debug("Waiting {} seconds to avoid blocking ...\n".format(wait_time))
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
logger.debug("Saving the data in {} file".format(output_filename))
with open(output_filename, 'w', encoding='utf-8') as outfile:
    json.dump(output_data, outfile, indent=4)
logger.debug("scraping finished")



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
- Contabilizar o tempo total
- Criar o container

"""