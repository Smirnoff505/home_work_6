from django.core.management import BaseCommand

from catalog.models import Category, Product
from django.core.management import call_command


class Command(BaseCommand):
    Category.objects.all().delete()
    Product.objects.all().delete()

    def handle(self, *args, **options):
        call_command('loaddata', 'data.json')
