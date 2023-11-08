from django.shortcuts import render


def home(request):
    return render(request, 'catalog/home.html')


def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        with open('info.txt', 'a', encoding='utf-8') as f:
            f.write(f'Имя: {name}\nТелефон: {phone}\nСообщение: {message}\n')
    return render(request, 'catalog/contacts.html')
