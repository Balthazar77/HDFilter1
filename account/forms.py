from django import forms
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth import forms as auth_forms
from django.forms import ClearableFileInput
from django.utils.translation import gettext_lazy as _


User = get_user_model()


class SignUpForm(auth_forms.UserCreationForm):
    password1 = forms.CharField(
        label='Пароль',
        help_text='Это поле обязательно',
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Пароль',
                'class': 'form-control'
            }
        )
    )
    password2 = forms.CharField(
        required=True,
        label='Пароль',
        help_text='Это поле обязательно',
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Повторить пароль',
                'class': 'form-control'
            }
        )
    )
    email = forms.EmailField(
        max_length=254,
        required=True,
        help_text='Это поле обязательно',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'E-mail',
                'class': 'form-control',
                'type' : 'email'
            }
        )
    )
    username = forms.CharField(
        max_length=254,
        required=True,
        label='Имя пользователя',
        help_text='Это поле обязательно',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Имя пользователя',
                'class': 'form-control',
                'type' : 'username'
            }
        )
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    @property
    def password(self):
        # call after is_valid()
        return self.cleaned_data['password1']

    def clean(self):
        super().clean()
        email = self.cleaned_data['email']
        already_exists = User.objects.filter(email=email).exists()

        if already_exists:
            raise forms.ValidationError(
                f'Пользователь с почтой {email} уже зарегистрирован',
                code='email_exists',
            )


class SetPasswordForm(auth_forms.SetPasswordForm):
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )


class ProfileForm(forms.ModelForm):

    first_name = forms.CharField(
        label='Имя',
        max_length=50,
        required=False,
        help_text='',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Имя',
                'class': 'form-control',
                'type': 'text',
            }
        ))
    last_name = forms.CharField(max_length=50,
        label='Фамилия',
        required=False,
        help_text='',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Фамилия',
                'class': 'form-control',
                'type': 'text',
            }
        ))
    email = forms.CharField(max_length=50,
        label='Электронная почта',
        required=False,
        help_text='',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Электронная почта',
                'class': 'form-control',
                'type': 'text',
            }
        ))
    telephone = forms.CharField(max_length=50,
        label='Телефон',
        required=False,
        help_text='',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Телефон',
                'class': 'form-control',
                'type': 'text',
            }
        ))
    name_org = forms.CharField(max_length=50,
        label='Наименнование организации',
        required=False,
        help_text='',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Наименнование организации',
                'class': 'form-control',
                'type': 'text',
            }
        ))
    name_director = forms.CharField(max_length=50,
        label='Генеральный директор',
        required=False,
        help_text='',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Генеральный директор',
                'class': 'form-control',
                'type': 'text',
            }
        ))
    ur_address = forms.CharField(max_length=50,
        label='Юридический адрес',
        required=False,
        help_text='',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Юридический адрес',
                'class': 'form-control',
                'type': 'text',
            }
        ))
    fk_address = forms.CharField(max_length=50,
        label='Фактический адрес',
        required=False,
        help_text='',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Фактический адрес',
                'class': 'form-control',
                'type': 'text',
            }
        ))
    inn = forms.CharField(max_length=50,
        label='ИНН',
        required=False,
        help_text='',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'ИНН',
                'class': 'form-control',
                'type': 'text',
            }
        ))
    kpp = forms.CharField(max_length=50,
        label='КПП',
        required=False,
        help_text='',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'КПП',
                'class': 'form-control',
                'type': 'text',
            }
        ))
    ogrn = forms.CharField(max_length=50,
        label='ОГРН',
        required=False,
        help_text='',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'ОГРН',
                'class': 'form-control',
                'type': 'text',
            }
        ))
    okpo = forms.CharField(max_length=50,
        label='ОКПО',
        required=False,
        help_text='',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'ОКПО',
                'class': 'form-control',
                'type': 'text',
            }
        ))
    okvid = forms.CharField(max_length=50,
        label='ОКВЭД',
        required=False,
        help_text='',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'ОКВЭД',
                'class': 'form-control',
                'type': 'text',
            }
        ))
    name_bank = forms.CharField(max_length=50,
        label='Название банка',
        required=False,
        help_text='',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Название банка',
                'class': 'form-control',
                'type': 'text',
            }
        ))
    bic = forms.CharField(max_length=50,
        label='БИК',
        required=False,
        help_text='',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'БИК',
                'class': 'form-control',
                'type': 'text',
            }
        ))
    r_chet = forms.CharField(max_length=50,
        label='Р/счет',
        required=False,
        help_text='',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Р/счет',
                'class': 'form-control',
                'type': 'text',
            }
        ))
    k_chet = forms.CharField(max_length=50,
        label='Корр.счет',
        required=False,
        help_text='',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Корр.счет',
                'class': 'form-control',
                'type': 'text',
            }
        ))
    post_address = forms.CharField(max_length=50,
        label='Почтовый адрес',
        required=False,
        help_text='',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Почтовый адрес',
                'class': 'form-control',
                'type': 'text',
            }
        ))
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'telephone','name_org','name_director')#'email',

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data
