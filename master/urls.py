"""master URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
import administration.views
import aliexpress.views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # AliExpress
    url(r'^search_aliexpress/', aliexpress.views.search),
    url(r'^home_aliexpress/', aliexpress.views.home),  
    # indexes
    url(r'^index_1/', aliexpress.views.index_1),
    url(r'^index_2/', aliexpress.views.index_2),      
]
