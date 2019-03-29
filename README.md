# Scraping findadentist.ada.org

This projects contains a set of scripts used to scrape dentist's data from findadentist.ada.org.

For this task I use Python and Selenium framework.

## Prerequisites

To run the scripts, download Python 3 from [Python.org](https://www.python.org/). 
After install, you need to install some Python packages:
```
pip install -r requirements.txt

```
## Usage

Script name: findadentist.py

This script perform a google search on linkedin based on some keywords and scrape all profiles showed in results. 

Supported parameters defined in the *paramaters.py* file:
* *max_number_of_profiles* - number of profiles that will be scraped.
* *debug* - if set to True the user data will be showed on the terminal/console.
* *useheadless* - if set to False, the script will not open the web browser (chrome).
* *search_query* - define the keywords to be used in the google search query.
```
# This search query will use the "python developer" and "London" keywords
search_query = 'site:linkedin.com/in/ AND "python developer" AND "London"'
```
* *file_name* - set the output file name.
* *linkedin_username* - set the username to login in the linkedin.
* *linkedin_password* - set the password.

Usage:
```
python linkedin_profiles_from_google.py
```

Output example:


