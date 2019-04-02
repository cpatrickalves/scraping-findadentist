# Scraping findadentist.ada.org

This project contains a set of Python scripts used to scrape the dentist's data from findadentist.ada.org.

## Prerequisites

To run the scripts, download Python 3 from [Python.org](https://www.python.org/). 
After install, you need to install some Python packages.

Open the terminal/Prompt/cmd and run:
```
pip install -r requirements.txt

```
## Usage

Script name: **findadentist.py**

```
python findadentist.py data/input2.json

```

This script performs several requests to the *findadentist.ada.org API* to get the dentist's data.
To obtain the data, the script performs the following tasks:
1. The scripts use a JSON input file with a set of "location", "zip code", "distance" and "specialty" parameters. 
2. For each set of parameters, the scripts perform a search for dentist's using *findadentist.ada.org API*. 
3. From the search results, the script takes a list of dentist's address Ids.
4. For each address Id, the script performs a new request to the *findadentist.ada.org API* and get the dentist's data.
5. Finally, the script formats the output data and save it in a JSON file (*output.json*).

In the **data/** folder you can find an example of the input and output files.

### Proxy Setup:

The *findadentist.ada.org* website has strong mechanisms against web scraping. 
So to get all the data you need to use some rotation proxy solution.

The Python file *proxy_pool.py* enables the use of a pool of proxies from two services: 
* https://www.sslproxies.org/
* https://proxycrawl.com      

The *sslproxies.org* contains a large list of public proxy servers that are updated every minute.
The **proxy_pool.py** builds a list of the last 100 proxy servers from *sslproxies.org*.

The *proxycrawl.com* service ([ProxyCrawl Backconnect Proxy](https://proxycrawl.com/scraping-with-worldwide-backconnect-proxy)) provides a unique address that receives all connections and automatically deals with the IP address rotation so that every request will use a different IP address. This service has better performance, but in the free version, you need to manually add your current IP address in the IP Whitelist through the website.

In the **findadentist.py** file there is a parameter called *proxy_server_options* used to set how to build your requests, the number set in this variable defines which proxy service will be used:

* *0* - Do not use Proxy
* *1* - Uses proxycrawl.com service (recommended)
* *2* - Uses sslproxies.org service (default option)

### Running an example::

In this example, I set *proxy_server_options = 1*.

```
>> scraping-findadentist>python findadentist.py data/input2.json
[I 190402 11:11:30 findadentist:131] Starting findadentist.py script ...
[D 190402 11:11:30 proxy_pool:24] Using proxy servers from proxy.proxycrawl.com
[I 190402 11:11:30 findadentist:136] Loading input file: data/input2.json
[I 190402 11:11:30 findadentist:173] Performing search 1/4 - requested page: https://findadentist.ada.org/api/Dentists?Address=30311&Specialty=1&Distance=5
[I 190402 11:11:33 findadentist:187] 18 dentists found.
[I 190402 11:11:33 findadentist:173] Performing search 2/4 - requested page: https://findadentist.ada.org/api/Dentists?Address=77478&Specialty=10&Distance=1
[W 190402 11:11:35 findadentist:184] No results found for the search parameters: Address=77478  Specialty=10  Distance=1
[I 190402 11:11:35 findadentist:173] Performing search 3/4 - requested page: https://findadentist.ada.org/api/Dentists?Address=90014&Specialty=6&Distance=1
[I 190402 11:11:38 findadentist:187] 7 dentists found.
[I 190402 11:11:38 findadentist:173] Performing search 4/4 - requested page: https://findadentist.ada.org/api/Dentists?Address=30311&Specialty=1&Distance=5
[I 190402 11:11:40 findadentist:187] 18 dentists found.
[I 190402 11:11:40 findadentist:194] A total of 25 dentists IDs obtained
[I 190402 11:11:40 findadentist:202] Getting data for 25 dentists
[I 190402 11:11:40 findadentist:205] Getting data for dentist ID 3463667 - 1/25
[I 190402 11:11:42 findadentist:205] Getting data for dentist ID 3753856 - 2/25
[I 190402 11:11:45 findadentist:205] Getting data for dentist ID 2965488 - 3/25
[I 190402 11:11:47 findadentist:205] Getting data for dentist ID 2803858 - 4/25
[I 190402 11:11:50 findadentist:205] Getting data for dentist ID 1538580 - 5/25
[I 190402 11:11:52 findadentist:205] Getting data for dentist ID 3279660 - 6/25
[I 190402 11:11:54 findadentist:205] Getting data for dentist ID 1648025 - 7/25
[I 190402 11:11:56 findadentist:205] Getting data for dentist ID 3433737 - 8/25
[I 190402 11:11:59 findadentist:205] Getting data for dentist ID 1648024 - 9/25
[I 190402 11:12:01 findadentist:205] Getting data for dentist ID 3063875 - 10/25
[I 190402 11:12:04 findadentist:205] Getting data for dentist ID 1647911 - 11/25
[I 190402 11:12:06 findadentist:205] Getting data for dentist ID 3500185 - 12/25
[I 190402 11:12:09 findadentist:205] Getting data for dentist ID 1464724 - 13/25
[I 190402 11:12:11 findadentist:205] Getting data for dentist ID 3278244 - 14/25
[I 190402 11:12:14 findadentist:205] Getting data for dentist ID 1562452 - 15/25
[I 190402 11:12:16 findadentist:205] Getting data for dentist ID 2757264 - 16/25
[I 190402 11:12:18 findadentist:205] Getting data for dentist ID 1647899 - 17/25
[I 190402 11:12:20 findadentist:205] Getting data for dentist ID 1519665 - 18/25
[I 190402 11:12:23 findadentist:205] Getting data for dentist ID 2770283 - 19/25
[I 190402 11:12:25 findadentist:205] Getting data for dentist ID 3518558 - 20/25
[I 190402 11:12:28 findadentist:205] Getting data for dentist ID 1538919 - 21/25
[I 190402 11:12:31 findadentist:205] Getting data for dentist ID 1538897 - 22/25
[I 190402 11:12:33 findadentist:205] Getting data for dentist ID 2770329 - 23/25
[I 190402 11:12:35 findadentist:205] Getting data for dentist ID 1619644 - 24/25
[I 190402 11:12:38 findadentist:205] Getting data for dentist ID 1620861 - 25/25
[D 190402 11:12:40 findadentist:244] Saving the data in output.json file
[I 190402 11:12:40 findadentist:250] Total scraping time: 1.16 minutes
[D 190402 11:12:40 findadentist:251] scraping finished

```

## License

This project is licensed under the Apache License Version 2.0 - see the [LICENSE.md](LICENSE) file for details.