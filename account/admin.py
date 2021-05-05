from django.contrib import admin
from django import forms

from account.models import User, DataUserOrganization


class AccountForm(forms.ModelForm):
    pass

@admin.register(User)
class AdminUser(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'telephone')
    list_display_links = ('username',)

@admin.register(DataUserOrganization)
class AdminUrOrganization(admin.ModelAdmin):
    list_display = ('name_org', 'name_director', 'inn')
    list_display_links = ('name_org',)