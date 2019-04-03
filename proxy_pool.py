# -*- coding: utf-8 -*-
#==============================================================================
#title           :proxy_pool.py
#description     :Get a list of proxy servers.
#author          :Patrick Alves (cpatrickalves@gmail.com)
#date            :01-04-2019
#python_version  :3.6
#==============================================================================

import requests
import proxy_pool
from logzero import logger
from bs4 import BeautifulSoup
from itertools import cycle

# Set the Proxy server to be used:
# 1 - Uses proxy.proxycrawl.com service
# 2 - Uses www.sslproxies.org service

# Function that gets a list of HTTPS proxies from https://www.sslproxies.org/ or https://proxycrawl.com      
def get_proxies_pool(proxy_server_options):    
    # Using Proxy Crawl service (recommended)
    if proxy_server_options == 1:
        logger.debug("Using proxy servers from proxy.proxycrawl.com")
        return cycle(['proxy.proxycrawl.com:9000'])
    
    # Using SSL proxies service
    elif proxy_server_options == 2:
        proxy_server_url = 'https://www.sslproxies.org/'
        logger.debug("Using proxy servers from {}".format(proxy_server_url))
        response = requests.get(proxy_server_url)
        if response.status_code != 200:
            logger.error('Failed to get Proxies list in {}'.format(proxy_server_url))

        soup = BeautifulSoup(response.text,"html.parser")
        # Filter to get only HTTPS proxies
        https_proxies = filter(lambda item: "yes" in item.text,
                            soup.select("table.table tr"))
        # Create a proxies list
        proxy_pool = []
        for item in https_proxies:
            proxy_pool.append("{}:{}".format(item.select_one("td").text,
                                item.select_one("td:nth-of-type(2)").text))
        
        return cycle(proxy_pool)
