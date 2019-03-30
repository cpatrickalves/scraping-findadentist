# Scraping findadentist.ada.org

This project contains a Python script used to scrape the dentist's data from findadentist.ada.org.

## Prerequisites

To run the scripts, download Python 3 from [Python.org](https://www.python.org/). 
After install, you need to install some Python packages.
Open the terminal/Prompt/cmd and run:
```
pip install -r requirements.txt

```
## Usage

Script name: findadentist.py

```
python findadentist.py data/input.json

```

This script performs several requests to the findadentist.ada.org API to get the dentist's data.
To obtain the data, the script performs the following tasks:
1. The scripts uses a JSON input file with a set of "location", "zip code", "distance" and "specialty" parameters. 
2. For each set of parameters, the scripts perform a search for dentist's using findadentist.ada.org API. 
3. From the search results, the script takes the dentist's address Ids.
4. For each address Id, the script performs a new request to the findadentist.ada.org API and get the dentist's data.
5. Finally, the script formats the output data and save it in a JSON file.

In the **data/** folder you can find a example of the input and output files.

### Execution example:

????




