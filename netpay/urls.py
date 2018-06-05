from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^process/$', views.payment_netpay, name='payment_netpay')    
]
