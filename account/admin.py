from django.contrib import admin
from django import forms
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils.safestring import mark_safe

from account.models import User, DataUserOrganization
from store.models import Product


class AccountForm(forms.ModelForm):
    pass

@admin.register(User)
class AdminUser(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'telephone')
    list_display_links = ('username',)

@admin.register(DataUserOrganization)
class AdminUrOrganization(admin.ModelAdmin, forms.ModelForm):
    list_display = ('name_org', 'name_director', 'inn')
    list_display_links = ('name_org',)

class RekvizitAdminForm(AdminUrOrganization):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['inn'].buttons = mark_safe(
            """<button type="submit" class="btn btn-success">Заполнить по инн</button>
            """)
#admin.site.unregister(Group)
