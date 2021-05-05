# Generated by Django 3.2 on 2021-05-04 12:15

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('role', models.IntegerField(choices=[(1, 'Менеджер'), (2, 'Клиент'), (3, 'Администратор')], default=2)),
                ('username', models.CharField(max_length=191, unique=True, verbose_name='Имя пользователя')),
                ('first_name', models.CharField(max_length=20, verbose_name='Имя')),
                ('last_name', models.CharField(max_length=30, verbose_name='Фамилия')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='Электронная почта')),
                ('telephone', models.CharField(max_length=30, verbose_name='Телефон')),
                ('is_staff', models.BooleanField(default=False, verbose_name='Доступ к админке')),
                ('is_activ', models.BooleanField(default=True, verbose_name='Активная учетная запись')),
                ('last_login', models.DateTimeField()),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
            ],
            options={
                'verbose_name': 'Аккаунт',
                'verbose_name_plural': 'Аккаунт',
            },
        ),
        migrations.CreateModel(
            name='DataUserOrganization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_org', models.CharField(max_length=150, verbose_name='Наименнование органицазии')),
                ('name_director', models.CharField(max_length=191, verbose_name='Генеральный директор')),
                ('ur_address', models.CharField(max_length=191, verbose_name='Юридический адрес')),
                ('fk_address', models.CharField(max_length=191, verbose_name='Фактический адрес')),
                ('ogrn', models.CharField(max_length=13, verbose_name='ОГРН')),
                ('inn', models.CharField(max_length=10, verbose_name='ИНН')),
                ('kpp', models.CharField(max_length=9, verbose_name='КПП')),
                ('okpo', models.CharField(max_length=10, verbose_name='ОКПО')),
                ('r_chet', models.CharField(max_length=10, verbose_name='Р/счет')),
                ('k_chet', models.CharField(max_length=10, verbose_name='Корр.счет')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.user')),
            ],
            options={
                'verbose_name': 'Реквизиты',
                'verbose_name_plural': 'Реквизиты',
            },
        ),
    ]