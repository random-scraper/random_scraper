# Required packages

import requests
from bs4 import BeautifulSoup
import re
from lxml.html import fromstring
import time
import random
import numpy as np
from requests.exceptions import ProxyError, Timeout
import time
from numpy.random import randint


def get_proxies(): #Scrape the proxies from website
    url = 'https://free-proxy-list.net/'
    response = requests.get(url)
    parser = fromstring(response.text)
    proxies = set()
    idx=1
    for i in parser.xpath('//tbody/tr')[0:300]:
            #Grabbing IP and corresponding PORT
        proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
        proxies.add(proxy)
        print(idx)
        idx+=1
    return proxies 

# Function to remove proxies that are not working
def update_proxies(candidate_proxies,proxy_remove): 
    candidate_proxies=candidate_proxies.difference(proxy_remove)
    while len(candidate_proxies)<2:
        candidate_proxies=get_proxies().difference(proxy_remove)
        time.sleep(5)
    return candidate_proxies

# Open file containing user agents

# Function to request page
def request_page(login_url,candidate_proxies,user_agents_file):
    with open(user_agents_file, 'r') as f: 
    candidate_user_agents = set(f.read().splitlines())
    bol=-100
    proxy_remove=set()
    while bol != 200:
            try:
                proxy=random.sample(candidate_proxies,1)[0]
                s=requests.session()
                page = s.get(login_url,
                                proxies={'http':proxy},
                                headers = {'User-Agent': random.sample(candidate_user_agents,1)[0]},timeout=10,allow_redirects=False)
                bol=page.status_code
                print(bol)
                candidate_proxies=update_proxies(candidate_proxies,set(proxy))
            except ProxyError:
                print("ProxyError")
                proxy_remove.add(proxy)
                candidate_proxies=update_proxies(candidate_proxies,proxy_remove)
                pass
            except Timeout:
                print("TimeOut")
                proxy_remove.add(proxy)
                candidate_proxies=update_proxies(candidate_proxies,proxy_remove)
                pass
            except requests.exceptions.RequestException as e:
                print("OtherError")
                print(e)
                time.sleep(5)
    return page,proxy_remove