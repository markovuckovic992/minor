import requests
import traceback
file = open('succeded.txt', 'r')
array = file.read().split()


for data in array:
    proxies = {'http': data, 'https': data}
    try:
        r = requests.get('http://google.com', proxies=proxies)
        msg = unicode(r.elapsed.total_seconds()) + '\n'
    except:
        print traceback.format_exc()
        msg = 'failed\n'
    f = open('resp.txt', 'a')
    f.write(msg)
    f.close()
