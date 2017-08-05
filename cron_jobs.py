#!/usr/bin/python
# -*- coding: utf-8 -*-
import django
import sys
import os
import pytz
from datetime import datetime
from aliexpress.fetch import main
os.environ['DJANGO_SETTINGS_MODULE'] = 'master.settings'
django.setup()
from administration.models import Users

class CronJobs:
    def __init__(self):
        pass

    def doFetch(self):
    	dt = pytz.timezone('UTC').localize(datetime.now())
        Users.objects.filter(datetime__lt=dt).delete()


c_j = CronJobs()
if len(sys.argv) > 1:
    if sys.argv[1] == 'fetch':
        c_j.doFetch()
