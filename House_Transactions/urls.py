"""House_Transactions URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from buyer.views import *
from seller.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexBuyer.as_view(), name='index'),
    path('login_buyer/', LoginBuyer.as_view(), name='login_buyer'),
    path('logout_buyer/', LogoutBuyer.as_view(), name='logout_buyer'),
    path('register_buyer/', RegisterBuyer.as_view(), name='register_buyer'),
    path('home_buyer/', HomeBuyer.as_view(), name='home'),
]
