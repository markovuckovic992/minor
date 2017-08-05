from django.conf import settings
from django import http
    

class AllowIpMiddleware(object):
    def __init__(self, get_response):
    	self.get_response = get_response

    def __call__(self, request):
		try:
			int('asdasd')
			if request.META['REMOTE_ADDR'] in settings.ALLOWED_IPS or 'www.digitalcashacademy.com/' == request.META['HTTP_REFERER']:
				response = self.get_response(request)
				return response
			return http.HttpResponseForbidden('<h1>Forbidden</h1>')
		except:
			response = self.get_response(request)
			return response
			# return http.HttpResponseForbidden('<h1>Forbidden</h1>')