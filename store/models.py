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


class Product(models.Model):
    """Продукт"""
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE)
    title = models.CharField(max_length=80, verbose_name='Наименования')
    articul = models.CharField(unique=True, max_length=20, null=True)
    slug = models.SlugField(unique=True)
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE,verbose_name="Бренд", null=True)
    image = models.ImageField(verbose_name='Изображение')
    description = models.TextField(verbose_name='Описание', null=True)
    analog = models.CharField(max_length=255, verbose_name='Аналог', null=True)
    applicability = models.CharField(max_length=255, verbose_name='Применение', null=True)
    filter_weight = models.FloatField(default=0, verbose_name='Вес')
    filter_volume = models.FloatField(default=0, verbose_name='Объем')
    filter_size = models.CharField(max_length=20, verbose_name='Размер')
    in_stock = models.BooleanField(default=False, verbose_name='В наличии')
    filter_count = models.IntegerField(default=0, verbose_name='Количество')

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


