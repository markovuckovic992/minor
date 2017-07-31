#!/usr/bin/env python
from bs4 import BeautifulSoup
import requests
import re
import json

class AliCrawler:
    def __init__(self):
        self.alidomain = 'aliexpress.com'

    def getItemById(self, item_id, store_stats=False, count=1):
        url = 'http://www.%s/item/-/%d.html' % (self.alidomain, item_id)
        req = requests.get(url)
        html = req.text
        bs4 = BeautifulSoup(html, "lxml")

        data = {}
        try:
            data['original_price'] = float(bs4.select('span[itemprop=highPrice]')[0].string.split(' ')[0])
        except:
            data['original_price'] = float(bs4.select('span[itemprop=price]')[0].string.split(' ')[0])            
     
        try:
            data['rating'] = float(bs4.select('span[itemprop=ratingValue]')[0].string)
        except:
            data['rating'] = 0.0

 
        try:
            content = bs4.select('span.shop-time')[0].em.text
            content = content.replace('year', '').replace('(s)', '')
            data['shop_time'] = int(content)
        except:
            data['shop_time'] = 0

        store = bs4.select('a.store-lnk')[0]
        data['store_id'] = int(bs4.select('#hid_storeId')[0].attrs['value'])

        #
        # offline
        #
        data['offline'] = True
        try:
            offline = re.findall('window.runParams.offline=(\w+);', html)[0]
            if offline == "false":
                data['offline'] = False
        except:
            pass

        #
        # store stats
        #
        if store_stats and not data['offline']:
            try:
                admin_id = int(re.findall('window.runParams.adminSeq="(\w+)";', html)[0])
                stats = self.getSellerStatsByAdminId(admin_id)
                data['store_points'] = stats
            except:
                data['store_points'] = None

        data['reviews'] = self.getSellerPositiveReviews(admin_id)
        #
        # shipping
        #
        data['free_shipping'] = False
        if not data['offline']:
            resp = self.getItemShippingById(item_id, count)
            data['free_shipping'] = resp[0]
            data['shipping_e'] = resp[1]

        return data

    def getItemShippingById(self, item_id, count):
        url = ('http://freight.%s/ajaxFreightCalculateService.htm'
            '?callback=json&f=d&userType=cnfm&country=US&count=%d'
            '&currencyCode=USD&productid=%d' % (self.alidomain, count, item_id))
        ePacket = False
        try:
            req = requests.get(url)
            data = json.loads(req.text[5:-1])
            prices = []
            for shipment in data['freight']:
                if shipment['companyDisplayName'] == 'ePacket':
                    ePacket = True
                prices.append(float(shipment['price']))
            shipping = min(prices)
        except:
            shipping = None

        return shipping == 0, ePacket

    def getSellerStatsByAdminId(self, admin_id):
        url = ('https://feedback.%s/display/evaluationDsrAjaxService.htm'
            '?callback=json&ownerAdminSeq=%d' % (self.alidomain, admin_id))

        try:
            req = requests.get(url)
            useful_data = req.text[8:-4].strip()
            tmp = json.loads(useful_data)
            data = 0
            i = 0
            for key in tmp.keys():
                data += float(tmp[key]['score'])
                i += 1
            data = data / i
            data = float("{0:.2f}".format(data))
        except:
            data = None 

        return data

    def getSellerPositiveReviews(self, admin_id):        
        url = ('https://feedback.%s/display/evaluationDetail.htm'
            '?callback=json&ownerMemberId=%d' % (self.alidomain, admin_id))
        req = requests.get(url)
        html = req.text
        bs4 = BeautifulSoup(html, "lxml")
        resp = bs4.select('a[class=fb-feedback-history-list]')[4].text
        resp = resp.replace('.', '').replace(',', '')
        return int(resp)

if __name__ == "__main__":
    ali = AliCrawler()
    ids = "1527079450,1600106660,1439525019,1439525019,1743878872,1435779436,1461847096"
    for id in ids.split(","):
        print "===== %d" % int(id)
        print ali.getItemById(int(id))
