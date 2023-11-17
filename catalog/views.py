from django.shortcuts import render

from catalog.models import Product, Contact


def home(request):
    last_product = Product.objects.order_by('data_creation')[:5]
    print(last_product)
    return render(request, 'catalog/home.html')


def contacts(request):
    contact = Contact.objects
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        with open('info.txt', 'a', encoding='utf-8') as f:
            f.write(f'Имя: {name}\nТелефон: {phone}\nСообщение: {message}\n')
    return render(request, 'catalog/contacts.html', {'contact': contact})
