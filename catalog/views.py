from django.shortcuts import render
from django.views.generic import ListView, DetailView

from catalog.models import Product, Contact


class ProductListView(ListView):
    """Просмотр всех объектов модели Product"""
    model = Product


def contacts(request):
    contact = Contact.objects
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        with open('info.txt', 'a', encoding='utf-8') as f:
            f.write(f'Имя: {name}\nТелефон: {phone}\nСообщение: {message}\n')
    return render(request, 'catalog/contacts.html', {'contact': contact})


class ProductDetailView(DetailView):
    """Просмотр одного объекта модели Product"""
    model = Product
