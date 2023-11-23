from django.shortcuts import render

from catalog.models import Product, Contact


def home(request):
    product_list = Product.objects.all()
    context = {
        'object_list': product_list
    }
    return render(request, 'catalog/home.html', context)


def contacts(request):
    contact = Contact.objects
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        with open('info.txt', 'a', encoding='utf-8') as f:
            f.write(f'Имя: {name}\nТелефон: {phone}\nСообщение: {message}\n')
    return render(request, 'catalog/contacts.html', {'contact': contact})


def product(request, pk):
    """
    Выводит станицу с описанием. На основании переданного PK
    """
    product_item = Product.objects.get(pk=pk)
    context = {
        'product': product_item
    }
    return render(request, 'catalog/product.html', context)
