from django.contrib import admin
from django import forms

from store.models import Category, Brand, Product


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
    list_display= ('id','title','articul','category','brand')
    list_display_links = ('title',)

#admin.site.register(Category)
