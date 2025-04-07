""""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from accounts.views import *
from S_image.views import *

urlpatterns = [
    path('l_page/', L_page ,name = "l_page"),
    path('R_page/', R_page ,name = "R_page"),
    path('l_out/', l_out ,name = "l_out"),
    path('about/', about ,name = "about"),
    path('encode/', encode_view, name='steganography'),
    path('decode/',decode_view, name='decode_image'),
    path('admin/', admin.site.urls)

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
