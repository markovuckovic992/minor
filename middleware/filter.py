from django.conf import settings
from django import http
from aliexpress.views import get_client_ip
from administration.models import Users

class AllowIpMiddleware(object):
    def __init__(self, get_response):
    	self.get_response = get_response

    def __call__(self, request):
		try:
			try:
				ip = unicode(get_client_ip(request))
				Users.objects.get(ip=ip)
				response = self.get_response(request)
				return response
			except:
				REFERER = request.META['HTTP_REFERER']
				if 'http://www.digitalcashacademy.com' in REFERER:
					response = self.get_response(request)
					return response
				elif 'http://138.201.226.93' in REFERER:					
					response = self.get_response(request)
					return response				
				elif 'https://www.ecomroad.com' in REFERER:					
					response = self.get_response(request)
					return response
				return http.HttpResponseForbidden(REFERER)
		except:
			return http.HttpResponseForbidden('<h1>Forbidden</h1>')