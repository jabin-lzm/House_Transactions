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

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexBuyer.as_view(), name='index'),
    path('login_buyer/', LoginBuyer.as_view(), name='login_buyer'),
    path('logout_buyer/', LogoutBuyer.as_view(), name='logout_buyer'),
    path('register_buyer/', RegisterBuyer.as_view(), name='register_buyer'),
    path('home_buyer/', HomeBuyer.as_view(), name='home_buyer'),

    path('login_seller/', LoginSeller.as_view(), name='login_seller'),
    path('logout_seller/', LogoutSeller.as_view(), name='logout_seller'),
    path('register_seller/', RegisterSeller.as_view(), name='register_seller'),
    path('home_seller/', HomeSeller.as_view(), name='home_seller'),
    path('seller_update', SellerUpdate.as_view(), name='seller_update'),
    path('my_houses/', MyHouses.as_view(), name='my_houses'),
    path('my_houses/create', HouseCreateView.as_view(), name='house_create'),
    path('my_houses/detail/<int:house_id>/', HouseDetailView.as_view(), name='house_detail'),
    path('my_houses/update/<int:house_id>/', HouseUpdateView.as_view(), name='house_update'),
    path('my_houses/delete/<int:house_id>/', HouseDeleteView.as_view(), name='house_delete'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
