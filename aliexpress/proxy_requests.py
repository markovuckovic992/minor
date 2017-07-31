import requests
from requests.exceptions import ConnectionError
import random
import os
import time
from bs4 import BeautifulSoup
from requests.exceptions import ReadTimeout
 
class RequestProxy:
    agent_file = 'user_agents.txt'

    def __init__(self, web_proxy_list=["http://54.207.114.172:3333"]):
       self.useragents = self.load_user_agents(RequestProxy.agent_file)
       #####
       # Proxy format:
       # http://<USERNAME>:<PASSWORD>@<IP-ADDR>:<PORT>
       #####
       self.proxy_list = web_proxy_list
       self.proxy_list += self.proxyForEU_url_parser('http://proxyfor.eu/geo.php', 100.0)
       self.proxy_list += self.freeProxy_url_parser('http://free-proxy-list.net')


    def load_user_agents(self, useragentsfile):
        useragents = []
        with open(useragentsfile, 'rb') as uaf:
            for ua in uaf.readlines():
                if ua:
                    useragents.append(ua.strip()[1:-1-1])
        random.shuffle(useragents)
        return useragents

    def get_random_user_agent(self):
        user_agent = random.choice(self.useragents)
        return user_agent

    def generate_random_request_headers(self):
        headers = {
        "Connection" : "close",  
        "User-Agent" : self.get_random_user_agent()} 
        return headers

    def proxyForEU_url_parser(self, web_url, speed_in_KBs=100.0):
        curr_proxy_list = []
        content = requests.get(web_url).content
        soup = BeautifulSoup(content, "html.parser")
        table = soup.find("table", attrs={"class": "proxy_list"})
 
        headings = [th.get_text() for th in table.find("tr").find_all("th")]
 
        datasets = []
        for row in table.find_all("tr")[1:]:
            dataset = zip(headings, (td.get_text() for td in row.find_all("td")))
            datasets.append(dataset)

        for dataset in datasets:
            proxy = "http://"
            proxy_straggler  = False
            for field in dataset:
                if field[0] == 'Speed':
                    if float(field[1]) < speed_in_KBs:
                        proxy_straggler = True
                if field[0] == 'IP':
                    proxy = proxy+field[1]+':'
                elif field[0] == 'Port':
                    proxy = proxy+field[1]
            if not proxy_straggler:
                curr_proxy_list.append(proxy.__str__())
        return curr_proxy_list

    def freeProxy_url_parser(self, web_url):
        curr_proxy_list = []
        content = requests.get(web_url).content
        soup = BeautifulSoup(content, "html.parser")
        table = soup.find("table", attrs={"class": "display fpltable"})
 
        headings = [th.get_text() for th in table.find("tr").find_all("th")]

        datasets = []
        for row in table.find_all("tr")[1:]:
            dataset = zip(headings, (td.get_text() for td in row.find_all("td")))
            datasets.append(dataset)

        for dataset in datasets:
            proxy = "http://"
            for field in dataset:
                if field[0] == 'IP Address':
                    proxy = proxy+field[1]+':'
                elif field[0] == 'Port':
                    proxy = proxy+field[1]
            curr_proxy_list.append(proxy.__str__())
        return curr_proxy_list


        def generate_proxied_request(self, url, params={}, req_timeout=30):
            if len(self.proxy_list) < 2:
                self.proxy_list += self.proxyForEU_url_parser('http://proxyfor.eu/geo.php')

            random.shuffle(self.proxy_list)
            req_headers = dict(params.items() + self.generate_random_request_headers().items())

            request = None
            try:
                rand_proxy = random.choice(self.proxy_list)
                request = requests.get(test_url, proxies={"http": rand_proxy}, headers=req_headers, timeout=req_timeout)
            except ConnectionError:
                self.proxy_list.remove(rand_proxy)
            except ReadTimeout:
                self.proxy_list.remove(rand_proxy)
            return request

if __name__ == '__main__':

    start = time.time()
    req_proxy = RequestProxy()
    test_url = 'http://www.aliexpress.com/item/-/32801386170.html'
    request = req_proxy.generate_proxied_request(test_url)
       