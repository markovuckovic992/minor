from django.shortcuts import render, HttpResponse

from alicrawler import AliCrawler

def home(request):
	return render(request, 'aliexpress.html', {})

def search(request):
	url = request.POST['url']
	url_array = url.split('.html')
	url = url_array[0]
	id = int(url.split('/')[-1])
	ali = AliCrawler()
	just_do_it = True
	i = 0
	while just_do_it:
		try:			
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



