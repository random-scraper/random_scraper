import requests
from lxml.html import fromstring
import time
import random
from requests.exceptions import ProxyError, Timeout
import os

def get_proxies(url='https://free-proxy-list.net/'): 
    """

    Scrape proxies from default url
    Args:
        url (str): url of proxy list
    Returns:
        list of proxies
    """

    response = requests.get(url)
    parser = fromstring(response.text)
    proxies = set()
    idx=1
    for i in parser.xpath('//tbody/tr')[0:300]:
            #Grabbing IP and corresponding PORT
        proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
        proxies.add(proxy)
        idx+=1
    return proxies 

def update_proxies(candidate_proxies,proxy_remove): 
    """

    Removes proxies that do not work
    Args:
        candidate_proxies (list): list of available proxies
        proxy_remove (list): list of proxies to remove
    Returns:
        list of proxies
    """

    candidate_proxies=candidate_proxies.difference(proxy_remove)
    while len(candidate_proxies)<2:
        candidate_proxies=get_proxies().difference(proxy_remove)
    return candidate_proxies

def candidate_user_agents():
    """
    
    Open file containing user agents
    Args:
        None
    Returns:
        candidate_user_agents (list): list of user agents
    """
    path_to_user_agents= os.path.join(os.path.dirname(__file__), "package_data", "user-agents.txt")
    with open(path_to_user_agents, 'r') as f: 
        user_agents = set(f.read().splitlines())
    return user_agents


def request_page(login_url,candidate_proxies=get_proxies(),candidate_user_agents=candidate_user_agents(),time_sleep_min=0,time_sleep_max=60):
    """

    Function to request page
    Args: 
        login_url (str): url to request for scrapign
        candidate_proxies (list): list of proxies available
        candidate_user_agents (list): list of user agents available
        time_sleep_min (float): Minimum amount of time to wait after an unsuccesful request
        time_sleep_max (float): Maximum amount of time to wait after an unsuccesful request
    Returns:
        page: page to scrape
        proxy_remove: list of proxies to remove for next iteration
    """

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
                time.sleep(random.random()*(time_sleep_max-time_sleep_min)+time_sleep_min)
    return page,proxy_remove