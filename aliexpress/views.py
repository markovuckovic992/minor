from django.shortcuts import render, HttpResponse

from administration.models import Users

from alicrawler import AliCrawler
from fetch import main

from datetime import datetime, timedelta
import random
import requests
import json

def get_client_ip(request):
	x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
	if x_forwarded_for:
		ip = x_forwarded_for.split(',')[0]
	else:
		ip = request.META.get('REMOTE_ADDR')
	return ip

def home(request):
	time = datetime.now() + timedelta(minutes=1)
	Users(ip=get_client_ip(request), datetime=time).save()
	return render(request, 'aliexpress.html', {})

def search(request):
    # POST DATA
    url = request.POST['url']
    price = request.POST['price']
    keys = request.POST.keys()
    r = True if 'r' in keys else False
    r_p = True if 'r_p' in keys else False
    b = True if 'b' in keys else False
    d_t_b = True if 'd_t_b' in keys else False
    s_b = True if 's_b' in keys else False
    g = True if 'g' in keys else False
    # END POST DATA
    file = open('json.json', 'r')
    proxies = list(json.loads(file.read()))
    file.close()
    # proxies = main()

    url_array = url.split('.html')
    url = url_array[0]
    try:
        id = int(url.split('/')[-1])
    except:
        data = url.split('/')[-1]
        id = int(data.split('_')[-1])
    just_do_it = True
    i = 0
    while just_do_it:
        try:
            # find_normal = True
            # while find_normal:
            #     try:
            id_ = random.randint(0, len(proxies))
            ip_ = proxies[id_]
            # requests.get('http://google.com', proxies={'http': ip_})
            # find_normal = False
            print ip_
                # except:
                #     pass
            ali = AliCrawler(ip_)
            resp = ali.getItemById(id, store_stats=True, count=1)
            just_do_it = False
        except:
            i += 1
        if i == 7:
            just_do_it = False
    if i == 7:
        return render(request, 'aliexpress.html', {'error': 'System failed to find data for this product. Try again after a while.'})
    else:
        file = open('succeded.txt', 'a')
        file.write(ip_ + '\n')
        file.close()
        return render(request, 'aliexpress_response.html', {'response': resp})

