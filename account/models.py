from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone
from django.db import models


class UserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('role', get_user_model().CLIENT)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('role', get_user_model().ADMIN)
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):

    MANAGER = 1
    CLIENT = 2
    ADMIN = 3

    STAFF_ROLES = {MANAGER, ADMIN}
    _GLOBAL_ROLE_CHOICES = (
        (MANAGER, 'Менеджер'),
        (CLIENT, 'Клиент'),
        (ADMIN, 'Администратор'),
    )
    role = models.IntegerField(choices=_GLOBAL_ROLE_CHOICES, default=CLIENT)
    username = models.CharField(max_length=191, blank=False, verbose_name='Имя пользователя')
    first_name = models.CharField(max_length=20, blank=False, verbose_name='Имя')
    last_name = models.CharField(max_length=30, blank=False, verbose_name='Фамилия')
    email = models.EmailField(max_length=255, unique=True, blank=False, verbose_name='Электронная почта')
    telephone = models.CharField(max_length=30, verbose_name='Телефон')
    is_staff = models.BooleanField(default=False, verbose_name='Доступ к админке')
    is_activ = models.BooleanField(default=True, verbose_name='Активная учетная запись')
    last_login = models.DateTimeField('date joined', default=timezone.now)
    date_joined = models.DateTimeField('date joined', default=timezone.now)

    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'

    objects = UserManager()

    class Meta:
        verbose_name = 'Аккаунт'
        verbose_name_plural = 'Аккаунт'

    def __str__(self):
        return self.get_full_name()

    def has_module_perms(self, app_label):

        print(f'has_module_perms - app_label: {app_label}')
        return self.is_superuser or self.is_manager

    def has_perm(self, perm, obj=None):

        print(f'has_perm - perm: {perm} obj: {obj}')
        return self.is_superuser or self.is_manager

    def get_full_name(self):
        if not self.first_name:
            return self.get_short_name()
        return f'{self.first_name} {self.last_name}'

    def get_short_name(self):
        return self.first_name or self.email

    @property
    def is_superuser(self):
        return self.role == self.ADMIN

    @property
    def is_manager(self):
        return self.role == self.MANAGER


class DataUserOrganization(models.Model):

    account = models.ForeignKey(User, on_delete=models.CASCADE)
    name_org = models.CharField(max_length=150, verbose_name='Наименнование органицазии')
    name_director = models.CharField(max_length=191, verbose_name='Генеральный директор')
    ur_address = models.CharField(max_length=191, verbose_name='Юридический адрес')
    fk_address = models.CharField(max_length=191, verbose_name='Фактический адрес')
    ogrn = models.CharField(max_length=13, verbose_name='ОГРН')
    inn = models.CharField(max_length=10, verbose_name='ИНН')
    kpp = models.CharField(max_length=9, verbose_name='КПП')
    okpo = models.CharField(max_length=10, verbose_name="ОКПО")
    r_chet = models.CharField(max_length=10, verbose_name='Р/счет')
    k_chet = models.CharField(max_length=10, verbose_name='Корр.счет')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Реквизиты'
        verbose_name_plural = 'Реквизиты'


class Enrollment(models.Model):

    MANAGER = 1
    CLIENT = 2

    _ROLE_CHOICES = (
        (MANAGER, 'Менеджер'),
        (CLIENT, 'Клиент'),
    )

    _ROLES_TRANSLATION = dict(_ROLE_CHOICES)

    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='enrollments'  # user.enrollments
    )

    role = models.IntegerField(choices=_ROLE_CHOICES, default=CLIENT)

    class Meta:
        verbose_name = 'Данные организации'
        verbose_name_plural = 'Данные организации'

    def __str__(self):
        user_name = self.user.get_full_name()
        return f'ХЗ: "{user_name}" "{self.DataUserOrganization.name_org}"'

    @property
    def human_role(self):
        return self._ROLES_TRANSLATION[self.role]

    # PermissionsMixin


