import requests

proxies = {
    'http': 'http://136.243.104.212:3128'
}

response = requests.get("http://www.aliexpress.com/item/-/32787289774.html", proxies=proxies)

file = open('html.html', 'w')
file.write(response.text)
file.close()
