
from django.urls import path
from django.conf.urls import url
from store.views import ProductListView, ProductByCategory, ProductDetailView, CartView


urlpatterns = [
    url(r'cart/', CartView.as_view(), name='cart'),
    url(r'^$', ProductListView.as_view(), name='product'),
    url(r'^(?P<slug>[\w-]+)/$', ProductByCategory.as_view(), name='category'),
    url(r'^(?P<slug>[\w-]+)/(?P<articul>[\w-]+)/$', ProductDetailView.as_view(), name='product_detail'),


]