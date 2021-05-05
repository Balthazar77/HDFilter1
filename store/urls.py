
from django.urls import path
from django.conf.urls import url
from store.views import ProductListView, ProductByCategory, ProductDetailView

urlpatterns = [
    url(r'^$', ProductListView.as_view(), name='product'),
    url(r'^(?P<slug>[\w-]+)/$', ProductByCategory.as_view(), name='category'),
    url(r'^(?P<slug>[\w-]+)/(?P<articul>[\w-]+)/$', ProductDetailView.as_view(), name='product_detail')
]