from django.shortcuts import render, HttpResponse

from alicrawler import AliCrawler

def home(request):
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
	url_array = url.split('.html')
	url = url_array[0]
	id = int(url.split('/')[-1])
	just_do_it = True
	i = 0
	while just_do_it:
		try:
			ali = AliCrawler()
			resp = ali.getItemById(id, store_stats=True, count=1)
			just_do_it = False
		except:
			i += 1
		if i == 5:
			just_do_it = False
	if i == 5:
		return render(request, 'aliexpress.html', {'error': 'System failed to find data for this product. Try again after a while.'})
	else:
		return render(request, 'aliexpress_response.html', {'response': resp})



