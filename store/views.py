from django.shortcuts import render
from django.views.generic import DetailView, ListView
from .models import Category, Product, Brand
from django.db.models import F


class ProductListView(ListView):
    """Запрос ко БД ко всем полям """
    template_name = 'product.html'
    context_object_name = 'product'
    model = Product

    def get_queryset(self):
        queryset = super(ProductListView, self).get_queryset()
        return queryset.filter().all()[:10]

    """Функция запроса к БД для дополнительного отбражение катагория"""
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.all()
        return context


class ProductByCategory(ListView):

    template_name = 'product.html'
    context_object_name = 'category'
    model = Category
    slug_field = 'url'

    def get_queryset(self,**kwargs):
        #queryset = Product.objects.filter(slug='slug')
        queryset = Product.objects.filter(slug=F('slug'))
        return queryset