from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect, request, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView, ListView
from pyexpat.errors import messages


from account.forms import AddCart
from . import models
from .models import Category, Product, Brand, Customer, Cart, CartProduct
from django.db.models import F, Q


class ProductListView(ListView):
    """Запрос ко БД ко всем полям """
    template_name = 'base.html'
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

    template_name = 'base.html'
    context_object_name = 'product'
    model = Product
    slug_field = 'slug'

    def dispatch(self, request, *args, **kwargs):
        self.category = get_object_or_404(
            Category,
            slug=self.kwargs['slug']
        )
        print(get_object_or_404(
            Category,
            slug=self.kwargs['slug']
        ))
        return super(ProductByCategory, self). \
            dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.all()
        context['current_category'] = self.category
        return context

    def get_queryset(self):
        queryset = super(ProductByCategory, self).get_queryset()
        return queryset.filter(category=self.category).all()


class ProductDetailView(DetailView):
    template_name = 'product_detail.html'
    context_object_name = 'product'
    slug_field = 'articul'
    slug_url_kwarg = 'articul'
    model = Product

    def dispatch(self, request, *args, **kwargs):

        self.category = get_object_or_404(
            Category,
            slug=self.kwargs['slug']
        )
        self.articul = self.kwargs['articul']

        return super(ProductDetailView, self). \
            dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context['category'] = Category.objects.all()
        return context

    def get_absolute_url(self):
        return reverse('post', kwargs={'articul': self.articul, 'slug': self.category})

    def get_queryset(self):
        queryset = super(ProductDetailView, self).get_queryset()
        return queryset.filter(articul=self.articul)

    def post(self, request , *args, **kwargs):
        # if request.method == "POST":
        #     cart = request.POST.get("cart")
        #     # age = request.POST.get("age")		# получение значения поля age
        #     return HttpResponse('ДАну нахуй')
        # else:
        #     addcart = AddCart()
        #     return render(request, "cart.html", {"form": addcart})
        print('в пизду')
        return  #Response({"message": "Hello, world!"})




# class AddToCartView(View):
#     def get(self, request, *args, **kwargs):
#         print(kwargs.get('cart_product'))
#         print(kwargs.get('cart'))
#
#
#         # articul, product_slug = kwargs.get('articul'), kwargs.get('slug')
#         # customer = Customer.objects.get(user=request.user)
#         # cart= Cart.objects.get(owner=customer, in_order=False)
#         # content_type = ContentType.objects.get(model=articul)
#         # product = content_type.model_class().objects.get(slug=product_slug)
#         # cart_product, create = CartProduct.objects.get_or_create(
#         #     user=cart.owner, cart=cart, content_type=content_type, object_id=product.id, final_price=product.price
#         # )
#         # cart.products.add(cart_product)
#
#         return HttpResponseRedirect('/cart/$')


class CartView(View):

    def get(self, request, *args, **kwargs):
        customer = Customer.objects.get(user=request.user)
        cart = Cart.objects.get(owner=customer)
        context = {
            'cart': cart,
        }
        return render(request, 'cart.html', context)

