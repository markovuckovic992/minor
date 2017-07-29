# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse

import json
# Create your views here.
def home(request):
	return render(request, 'home.html')

def getLiveScore(request):
	return HttpResponse(json.dumps({
        "greeting": "Hello!",
    }))  
	# http://rezultati.soccerbet.rs/live_score_danas/