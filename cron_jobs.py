#!/usr/bin/python
# -*- coding: utf-8 -*-
import django
import sys
import os
from aliexpress.fetch import main
os.environ['DJANGO_SETTINGS_MODULE'] = 'master.settings'
django.setup()

class CronJobs:
    def __init__(self):
        pass

    def doFetch(self):
        main()


c_j = CronJobs()
if len(sys.argv) > 1:
    if sys.argv[1] == 'fetch':
        c_j.doFetch()
