from django.db import models
from pytils.translit import slugify


class Blog(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    body = models.TextField(verbose_name='Статья')
    slug = models.CharField(max_length=50, verbose_name='slug', null=True, blank=True, unique=True)
    preview = models.ImageField(upload_to='imj_blog/', verbose_name='Изображение', null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    is_publication = models.BooleanField(default=False, verbose_name='Опубликовано')
    views_count = models.IntegerField(verbose_name='Количество просмотров', default=0)

    def save(self, *args, **kwargs):
        """Переопределен метод save. При создании сущности сразу заполняется
        поле slug."""
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.title}, {self.create_date}, {self.is_publication}'

    class Meta:
        verbose_name = 'Блог'
