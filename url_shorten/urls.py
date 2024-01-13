"""url_shorten URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path

from url import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('/',views.home),
    path('signin/',views.add_signin_info),
    path('login/',views.login),
    path('verify/',views.verify_email),
    path('forget_pass/',views.forget_password),
    path('change_pass/',views.change_password),
    path('add_info/',views.add_info),
    path('long/',views.short_long),
    path('history/',views.user_history),
]
