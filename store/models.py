from PIL import Image
from django.db import models
from pytils.translit import slugify


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
    price = models.DecimalField(max_digits=9, decimal_places=2, default=0, verbose_name='Цена')
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

