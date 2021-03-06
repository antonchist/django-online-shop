from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.KatalogList, name='KatalogList'),
    url(r'^(?P<category_slug>[-\w]+)/$', views.ProductList, name='ProductListByCategory'),
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.ProductDetail, name='ProductDetail'),
]
