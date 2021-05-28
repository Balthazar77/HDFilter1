from PIL import Image
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse
from pytils.translit import slugify
from account.models import User


def get_models_for_count(*model_names):
    return [models.Count(model_names) for model_name in model_names]


def get_product_url(obj, viewname):
    ct_model = obj.__class__._meta.model_name
    return reverse(viewname, kwargs={'ct_model': ct_model, 'slug': obj.slug})
    pass


class LatestProductsManager:

    @staticmethod
    def get_products_for_main_page(*args, **kwargs):
        with_respect_to = kwargs.get('with_respect_to')
        products = []
        ct_models = ContentType.object.filter(model__in=args)
        for ct_model in ct_models:
            model_products = ct_model.model_class()._base_manager.all().order_by('-id')[:5]
            products.extend(model_products)
        if with_respect_to:
            ct_model = ContentType.objects.filter(model=with_respect_to)
            if ct_model.exists():
                if with_respect_to in args:
                    return sorted(
                        products, key=lambda x: x.__class__.meta.model_name.startswith(with_respect_to), reverse=True
                    )
        return products


class LatestProducts:
    objects = LatestProductsManager()



class Category(models.Model):
    """Категории"""
    name = models.CharField(max_length=80, verbose_name="Имя катергории")
    slug = models.SlugField(blank=True,unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = self.slug or slugify(self.name)
        super().save(*args,**kwargs)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Катергории'


class Brand(models.Model):
    """Бренд"""
    name = models.CharField(max_length=50, verbose_name="Бренд")
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        self.slug = self.slug or slugify(self.name)
        super().save(*args,**kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренд'


class MinResolutionErrorExceptins(Exception):
    pass


class MaxResolutionErrorExceptins(Exception):
    pass


class Product(models.Model):
    """Продукт"""
    MIN_RESOLUTION = (200, 200)
    MAX_RESOLUTION = (800, 800)
    MAX_IMAGE_SIZE = 3145728
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE)
    title = models.CharField(max_length=80, verbose_name='Наименования')
    articul = models.SlugField(unique=True, max_length=20, null=True)
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE,verbose_name="Бренд", null=True)
    image = models.ImageField(verbose_name='Изображение')
    description = models.TextField(verbose_name='Описание', null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Цена')
    analog = models.CharField(max_length=255, verbose_name='Аналог', null=True)
    applicability = models.CharField(max_length=255, verbose_name='Применение', null=True)
    filter_weight = models.FloatField(default=0, verbose_name='Вес')
    filter_volume = models.FloatField(default=0, verbose_name='Объем')
    filter_size = models.CharField(max_length=20, verbose_name='Размер')
    in_stock = models.BooleanField(default=False, verbose_name='В наличии')
    filter_count = models.IntegerField(default=0, verbose_name='Количество')

    def save(self, *args, **kwargs):
        image = self.image
        img = Image.open(image)
        min_height, min_width = Product.MIN_RESOLUTION
        max_height, max_width = Product.MAX_RESOLUTION
        if img.height < min_height or img.width < min_width:
            raise MinResolutionErrorExceptins('Разрешение избражения меньше минимального!')
        if img.height > max_height or img.width > max_width:
            raise MaxResolutionErrorExceptins('Разрешение избражения больше максимального!')
        # image = self.image
        # img = Image.open(image)
        # new_img = img.convert('RGB')
        # resized_new_img = new_img.resize((200, 200), Image.ANTIALIAS)
        # filestream = BytesIO()
        # resized_new_img.save(filestream, 'JPEG', quality=90)
        # filestream.seek(0)
        # name = '{}.{}'.format(*self.image.name.split('.'))
        # self.image = InMemoryUploadedFile(
        #     filestream, 'ImageField', name, 'jpeg/image', sys.getsizeof(filestream),None
        # )
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class CartProduct(models.Model):
    user = models.ForeignKey('Customer', verbose_name='Покупатель', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name='Корзина', on_delete=models.CASCADE, related_name='related_products')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    qty = models.PositiveIntegerField(default=1)
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Общая цена')

    def __str__(self):
        return "Продукт: {} (для корзины)".format(self.content_object.title)

    class Meta:
        verbose_name = "Карта продукта"
        verbose_name_plural = "Карты продуктов"


class Cart(models.Model):
    owner = models.ForeignKey('Customer', verbose_name='Владелец', on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct, blank=True, related_name='related_cart')
    total_products = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Общая цена')
    in_order = models.BooleanField(default=False)
    for_anonymous_user = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзина"


class Customer(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, verbose_name='Номер телефона')
    address = models.CharField(max_length=255, verbose_name='Адрес')

    def __str__(self):
        return "Покупатель {} {}".format(self.user.first_name, self.user.last_name)