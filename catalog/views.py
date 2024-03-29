from django.contrib.auth.decorators import permission_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from catalog.forms import ProductForm, VersionForm
from catalog.models import Product, Contact, Version, Category
from catalog.services import get_cached_categories


class ProductCreateView(LoginRequiredMixin, CreateView):
    """Создание продукта"""
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:products')

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()

        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование продукта"""
    model = Product
    form_class = ProductForm

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_staff:
            raise Http404
        return self.object

    def get_success_url(self):
        return reverse('catalog:update_product', args=[self.kwargs.get('pk')])

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = VersionFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = VersionFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        counter = 0
        formset = self.get_context_data()['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()

        for f in formset:
            if f.initial.get('is_current'):
                counter += 1
            else:
                continue
        if counter > 1:
            raise ValidationError('Активная версия может быть только одна')
        return super().form_valid(form)


class ProductListView(ListView):
    """Просмотр всех объектов модели Product"""
    model = Product

    def get_context_data(self, **kwargs):
        """Переопределение метода, version_set в коде является менеджером связей для модели Product,
        создается для всех моделей, имеющих связи ForeignKey (Это памятка для себя)"""
        # Вызываем родительский класс с данными
        context = super().get_context_data(**kwargs)

        for product in context['object_list']:
            active_version = product.version_set.filter(is_current=True).first()
            if active_version:
                product.active_version_number = active_version.version_number
            else:
                product.active_version_number = None
        return context


def contacts(request):
    contact = Contact.objects
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        with open('info.txt', 'a', encoding='utf-8') as f:
            f.write(f'Имя: {name}\nТелефон: {phone}\nСообщение: {message}\n')
    return render(request, 'catalog/contacts.html', {'contact': contact})


class ProductDetailView(LoginRequiredMixin, DetailView):
    """Просмотр одного объекта модели Product"""
    model = Product


@user_passes_test(lambda u: u.is_staff)
@permission_required('catalog.set_published')
def to_published(request, pk):
    """Функция для переключения статуса опубликованное/неопубликованное"""
    product_item = get_object_or_404(Product, pk=pk)
    if product_item.is_published:
        product_item.is_published = False
    else:
        product_item.is_published = True
    product_item.save()
    return redirect(reverse('catalog:view', args=[pk]))


class CategoryListView(ListView):
    """Просмотр всех объектов модели Category"""
    model = Category

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['categories'] = get_cached_categories()
        return context_data
