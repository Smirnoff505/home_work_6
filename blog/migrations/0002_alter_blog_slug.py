# Generated by Django 4.2.7 on 2023-12-02 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='slug',
            field=models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='slag'),
        ),
    ]
