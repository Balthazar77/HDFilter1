from django.contrib import admin
from django import forms

from store.models import Category, Brand, Product, CartProduct, Cart, Customer


class CategoryForm(forms.ModelForm):
    pass

@admin.register(Category)
class AdminCategory(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    list_display_links = ('name',)

@admin.register(Brand)
class AdminBrand(admin.ModelAdmin):
    list_display= ('id','name','slug')
    prepopulated_fields = {'slug': ('name',)}
    list_display_links = ('name',)

@admin.register(Product)
class AdminProduct(admin.ModelAdmin):
    list_display = ('id','title','articul','category','brand')
    list_display_links = ('title',)

# @admin.register(Cart)
# class AdminCart(admin.ModelAdmin):
#     list_display = ('id','owner','products','total_products','final_price')
#     list_display_links = ('owner',)
#
# @admin.register(CartProduct)
# class AdminCartProduct(admin.ModelAdmin):
#     list_display = ('id','user','object_id','final_price')
#     list_display_links = ('user')
#
# @admin.register(Customer)
# class AdminCustomer(admin.ModelAdmin):
#     list_display = ('user')
#     list_display_links = ('user',)

#admin.site.register(Category)
admin.site.register(CartProduct)
admin.site.register(Cart)
admin.site.register(Customer)