# Generated by Django 4.2.7 on 2023-11-30 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Заголовок')),
                ('body', models.TextField(verbose_name='Статья')),
                ('slug', models.CharField(blank=True, max_length=50, null=True, verbose_name='slag')),
                ('preview', models.ImageField(blank=True, null=True, upload_to='imj_blog/', verbose_name='Изображение')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('is_publication', models.BooleanField(default=False, verbose_name='Опубликовано')),
                ('views_count', models.IntegerField(default=0, verbose_name='Количество просмотров')),
            ],
            options={
                'verbose_name': 'Блог',
            },
        ),
    ]
