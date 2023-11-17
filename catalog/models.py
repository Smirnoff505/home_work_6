from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(upload_to='media/', verbose_name='Изображение', **NULLABLE)
    # category = models.CharField(max_length=150, verbose_name='Категория')
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    price = models.IntegerField(verbose_name='Цена')
    data_creation = models.DateField(verbose_name='Дата создания')
    last_modified_date = models.DateField(verbose_name='Дата последнего изменения')

    def __str__(self):
        return f'{self.name}, {self.description}'

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание')

    # created_at = models.CharField(verbose_name='create', **NULLABLE)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Contact(models.Model):
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилмя')
    phone = models.IntegerField(verbose_name='Телефон')

    def __str__(self):
        return f'{self.last_name} {self.first_name} Контактный номер:{self.phone}'

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'
