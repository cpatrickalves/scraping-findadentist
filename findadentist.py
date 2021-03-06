# -*- coding: utf-8 -*-
#==============================================================================
#title           :findadentist.py
#description     :Extract Dentist's profiles from the findadentist.ada.org website.
#author          :Patrick Alves (cpatrickalves@gmail.com)
#creation date   :29-03-2019
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
from datetime import datetime
from proxy_pool import get_proxies_pool


# Function that makes the requests to the findadentist.ada.org API
def make_request(url, proxy_pool, proxy_server_options):

    # Default number of seconds to wait between 
    wait_time = 2                                        

    # Creating the header to allow requests to the findadentist.ada.org API
    headers = { "Authorization": "Basic NUNtQitIcVZuOXhTVnFKNkhiZC8xSGZnb29NdU1ZaXk=",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
                "Referer": "https://findadentist.ada.org/search-results?specialty=1&address=90014&distance=100&searchResultsReferrer=true",
              }  

    # Number of times the script will retry a request after a error/blocking
    request_retries_limit = 10 
    if proxy_server_options == 2: request_retries_limit = 50 
    # Retries counter                                
    request_retries_counter = 0    

    # Using proxy        
    if proxy_pool != None:         
        while (True):
            # Get proxy IP address and Port            
            proxy = next(proxy_pool)               
            try:
                # Make request with proxy
                if proxy_server_options != 1: logger.debug("Using proxy: {}".format(proxy))                
                response = requests.get(url, headers=headers, proxies={"http": proxy, "https": proxy}, timeout=5)                                  
                
                # Check if the Proxy IP adress got blocked 
                dentist_profile_id_response = None
                if 'DentistProfile' in url:
                    dentist_profile_id_response = json.loads(response.text)['PersonId']
                if (dentist_profile_id_response == 0) or (response.text == '"Not found"'): 
                    logger.warn("Proxy server {} was blocked, trying a new one ...".format(proxy))                
                    continue
                else:
                    break
                
                # Wait some time to the next request
                sleep(wait_time/2)               

            # If got a error
            except:
                # Starts a random wait time and try the request again
                request_retries_counter += 1 
                # Wait some time and try again
                sleep(wait_time)               
                logger.warn("Proxy connection error, changing proxy ...")                                                
            
            # Check if the number of retries was reached
            if request_retries_counter >= request_retries_limit:
                logger.error("Retries limit reached - Can't connect to the proxy servers")
                logger.error("Closing the script.")
                sys.exit()
         
    # If no proxy was set
    else:            
        # Make request with no Proxy
        response = requests.get(url, headers=headers)    
        # Wait 1 seconds between requests
        sleep(wait_time)
                
        # SEARCH PROFILE requests
        # If you get blocked the reponse status code is 404 and the text in the
        # response is '"Not Found"'

        # DENTIST PROFILE requests
        # The reponse for the Dentist Profile API always got the 200 status code, but
        # if you get blocked it responses with a JSON with null values .
        # Get the Person ID of the JSON in the response
        # If was a request to the Dentist profiles:
        dentist_profile_id_response = None
        if 'DentistProfile' in url:
            dentist_profile_id_response = json.loads(response.text)['PersonId']

        while (dentist_profile_id_response == 0) or (response.text == '"Not found"'): 
            # Starts a random wait time and try the request again
            request_retries_counter += 1
            # Create a random timer based on the number of retries made
            random_wait_time = randint(15, 30) * request_retries_counter
            logger.warn("You got an unexpected response, you may have been blocked!")
            logger.warn("Waiting a random time: {} seconds ...".format(random_wait_time))
            sleep(random_wait_time)   
            logger.warn("Trying a new request: {}".format(url))
            response = requests.get(url, headers=headers)    

            # Check if the number of retries was reached
            if request_retries_counter >= request_retries_limit:
                logger.error("Retries limit reached - You may have been blocked, change your IP address and try again")
                logger.error("Closing the script.")
                sys.exit()

    return response


# Function that's performs search for dentists based on three parameters: specialty, Distance and Address
def search_dentists(input_data, proxy_server_options):

    # Setup Proxy
    proxy_pool = None
    if proxy_server_options != 0:     
        proxy_pool = get_proxies_pool(proxy_server_options)    

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
    search_results = {}                                     # Saves the dentists Ids, Distances and InputZip codes.
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
        response = make_request(url, proxy_pool, proxy_server_options)
        
        # Load the data in a dict object
        data = json.loads(response.text)
        
        # If no results found, show the message: “No result found”
        if 'Dentists' not in data.keys():
            logger.warn("No results found for the search parameters: Address={}  Specialty={}  Distance={}".format(inputs['zip code'], 
                                                                                                    specialty[inputs['specialty']], 
                                                                                                    inputs['distance']))
            continue
        
        logger.info("{} dentists found.".format(len(data["Dentists"])))

        # Saves the Address Ids as dict keys and Distances and InputZip codes a list.
        for dentist in data["Dentists"]:
            if dentist["AddressId"] not in search_results.keys():
                search_results[dentist["AddressId"]] = [dentist["Distance"], inputs['zip code']] 
            
    logger.info("A total of {} dentists IDs obtained".format(len(search_results)))

    return search_results


# This function receives a dict with dentists AddressID (as a dict key), distance and inputZip data taken
# from the search results and produce requests to the website API to get the data.
def get_dentists_data(search_results, proxy_server_options):
    # Scraping dentists data
    # Get the dentist's data from website API using the AddressIDs
    dentists_counter = 1
    dentists_data = [] # List object that saves the dentist's data

    # Setup Proxy
    proxy_pool = None
    if proxy_server_options != 0:     
        proxy_pool = get_proxies_pool(proxy_server_options)    

    # Scraping data for each dentist ID
    logger.info("Getting data for {} dentists".format(len(search_results)))
    for dentist_id in search_results.keys():
        # Make request
        logger.info("Getting data for dentist ID {} - {}/{}".format(dentist_id, dentists_counter, len(search_results)))
        dentists_counter += 1
        url = "https://findadentist.ada.org/api/DentistProfile?AddressId={}".format(dentist_id)
        response = make_request(url, proxy_pool, proxy_server_options)
            
        # Saving dentist's data
        data = json.loads(response.text)    
        # Put the data in JSON schema
        formated_data = {
                        "dentistName": data["Name"],
                        "specialty": data["Specialty"],
                        "profieImage_URL": data["Photo"],
                        "website": data["WebSite"],
                        "language": data["Languages"],
                        "education": data["Education"][0]["Name"],
                        "gender": data["Gender"],
                        "paymentOptions": data["PaymentOptions"],
                        
                        "contactInfo": 
                        {
                        "phone": data["Phone"],
                        "address": data["Address"],
                        "city": data["City"],
                        "state": data["State"],
                        "zip": data["Zip"]
                        },
                        "proximity": 
                        {
                        "distance": str(search_results[dentist_id][0]),
                        "inputZip": str(search_results[dentist_id][1])
                        }
                    }

        # Saving the data in the list
        dentists_data.append(formated_data)

    return dentists_data


# Main function
def main():
    # Check if the input file was in the command parameters
    if (len(sys.argv) < 2):
        logger.error("Missing input file! You need to pass the JSON input file as a script's parameter.")
        logger.error('<usage>: python findadentist.py inputfile.json')
        sys.exit()

    # Set the Proxy option to be used:
    # 0 - Do not use Proxy
    # 1 - Uses proxy.proxycrawl.com service (recommended)
    # 2 - Uses www.sslproxies.org service
    proxy_server_options = 2
   
    # Starting scraping
    start_time = datetime.today()
    logger.info('Starting findadentist.py script ...')
   
    # Load JSON file with input data
    logger.info("Loading input file: {}".format(sys.argv[1]))
    try:
        with open(sys.argv[1]) as json_file:  
            input_data = json.load(json_file)

    except Exception as exc:
        logger.error(str(exc))
        sys.exit()


    # Perform a search in the findadentist.ada.org using the parameters in JSON file
    search_results = search_dentists(input_data, proxy_server_options)
    # Get the dentist data from the search results
    dentists_data = get_dentists_data(search_results, proxy_server_options) 
        
    # Saving the data in a JSON file
    output_data = {"FindDentist_Output": dentists_data}
    output_filename = 'output.json'
    logger.debug("Saving the data in {} file".format(output_filename))
    with open(output_filename, 'w', encoding='utf-8') as outfile:
        json.dump(output_data, outfile, indent=4)

    # Compute scraping time
    time_elapsed = (datetime.today() - start_time).total_seconds()
    logger.info("Total scraping time: {} minutes".format(round(time_elapsed/60,2)))
    logger.debug("scraping finished")


# Running the script
if __name__ == "__main__":
    main()