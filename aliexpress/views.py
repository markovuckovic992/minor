from django.shortcuts import render, HttpResponse

from administration.models import Users

from alicrawler import AliCrawler
from fetch import main

from datetime import datetime, timedelta
import random
import requests
import json
import traceback

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def home(request):
    time = datetime.now() + timedelta(minutes=1)
    if not Users.objects.filter(ip=get_client_ip(request)).exists():
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
            # pass
            log = open('log.txt', 'a')
            log.write(traceback.format_exc() + '\n\n---------------------------\n\n')
            log.close()
            i += 1
        if i == 7:
            just_do_it = False
    if i == 7:
        return render(request, 'aliexpress.html', {'error': 'System failed to find data for this product. Try again after a while.'})
    else:
        resp, answers = make_real_response(resp, price, r, r_p, b, d_t_b, s_b, g)
        return render(request, 'aliexpress_response.html', {'response': resp, 'answers': answers})

# dict_ = {
#     'Price Markup': [
#         'GREAT! The markup is high enough.',
#         'HMM... The markup might not be high enough. Think twice before you go for it.',
#         'NOT RECOMMENDED! With this markup, we believe it\'s going to be hard to turn a profit. You might want to stay away from this product.'
#     ],
#     'Fulfillment Safety': [
#         'GREAT! It\'s all looking good. Fulfillment shouldn\'t be a problem.',
#         'MEH... Fulfillment might be a problem. We recommend you manually review the feedback and status of the store and then decide.',
#         'NOT RECOMMENDED! It doesn\'t look great. You might potentially have fulfillment headaches. Maybe you should stay away from this product.'
#     ],
#     'Shipping': [
#         'GREAT! Free shipping!',
#         'THIS WORKS... You\'re good with shipping!',
#         'NOT RECOMMENDED! It doesn\'t look like they offer either free shipping or ePacket. From our experience, other shipping methods might be troublesome and expensive, but you can check manually to see what\'s happening.'
#     ],
#     'CLV': [
#         'GREAT! It seems like if someone buys this product, they\'re likely to buy other similar products. That\'s good as it allows you to have a higher Customer Lifetime Value.',
#         'MEH... If it\'s hard to find other similar products that your audience would buy, then you might want to think twice. You want to be able to upsell, downsell and bundle to your audience.',
#         'NOT RECOMMENDED! If you can\'t see this product being used as an upsell or in a bundle, then you might want to stay away. Typically, it\'s easy to give other similar products to your niche. So you shouldn\'t go with products that don\'t lend themselves to upsells, bundling, etc...',
#     ],
#     'Trends': [
#         'GREAT! It\'s trending, it\'s especially popular during a major sales season, so it\'s all looking good!',
#         'NOT BAD! Not perfect, but also not bad. Think about it one more time and you feel that it\'s popular, go for it!',
#         'NOT RECOMMENDED! Doesn\'t look like it\'s very popular... Maybe you should stay away.',
#     ]
# }

dict_ = {
    'Price Markup': [
        0,
        1,
        2
    ],
    'Fulfillment Safety': [
        0,
        1,
        2
    ],
    'Shipping': [
        0,
        1,
        2
    ],
    'CLV': [
        0,
        1,
        2
    ],
    'Trends': [
        0,
        1,
        2
    ]
}


def make_real_response(resp, price, r, r_p, b, d_t_b, s_b, g):
    answers = 3
    counter = 0
    response = {}

    original_price = float(resp['original_price'])
    tmp = float(price) / original_price * 100
    if tmp < 200:
        answers = 2
        response.update({
            'p_m': dict_['Price Markup'][2]
        })
    elif tmp < 300:
        counter += 1
        response.update({
            'p_m': dict_['Price Markup'][1]
        })
    else:
        response.update({
            'p_m': dict_['Price Markup'][0]
        })

    p_r = resp['rating']
    sum = 0
    if float(p_r) > 4.5:
        sum += 1
    elif float(p_r) < 4.0:
        sum -= 1

    s_r = resp['store_points']
    if float(s_r) > 4.5:
        sum += 1
    elif float(s_r) < 4.0:
        sum -= 1

    rw = resp['reviews']
    if float(rw) >= 1000:
        sum += 2
    elif float(rw) >= 500:
        sum += 1

    yb = resp['shop_time']
    if float(rw) >= 2:
        sum += 2
    elif float(rw) >= 1:
        sum += 1

    if sum >= 4:
        response.update({
            'f_s': dict_['Fulfillment Safety'][0]
        })
    elif sum >= 2:
        counter += 1
        response.update({
            'f_s': dict_['Fulfillment Safety'][1]
        })
    else:
        answers = 2
        response.update({
            'f_s': dict_['Fulfillment Safety'][2]
        })



    sum = 0
    if resp['shipping_e']:
        sum += 1
    if resp['free_shipping']:
        sum += 1

    if sum >= 2:
        response.update({
            'Shipping': dict_['Shipping'][0]
        })
    elif sum >= 1:
        counter += 1
        response.update({
            'Shipping': dict_['Shipping'][1]
        })
    else:
        answers = 2
        response.update({
            'Shipping': dict_['Shipping'][2]
        })

    sum = 0
    if r:
        sum += 1
    if r_p:
        sum += 1
    if b:
        sum += 1

    if sum >= 3:
        response.update({
            'CLV': dict_['CLV'][0]
        })
    elif sum >= 2:
        counter += 1
        response.update({
            'CLV': dict_['Shipping'][1]
        })
    else:
        answers = 2
        response.update({
            'CLV': dict_['CLV'][2]
        })


    sum = 0
    if d_t_b:
        sum += 1
    if s_b:
        sum += 1
    if g:
        sum += 1

    if sum >= 3:
        response.update({
            'Trends': dict_['Trends'][0]
        })
    elif sum >= 2:
        counter += 1
        response.update({
            'Trends': dict_['Trends'][1]
        })
    else:
        answers = 2
        response.update({
            'Trends': dict_['Trends'][2]
        })


    if answers == 3:
        if counter <= 2:
            answer = 1
        else:
            answer = 0

    return response, answers


def index_2(request):
    return render(request, 'index_2.html', {})


def index_1(request):
    return render(request, 'index_1.html', {})
