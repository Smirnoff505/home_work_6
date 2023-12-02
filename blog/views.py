
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from blog.models import Blog


class BlogCreateView(CreateView):
    """Создание сущности с полями:
    title: str
    body: text
    preview: img"""
    model = Blog
    fields = ('title', 'body', 'preview',)
    success_url = reverse_lazy('blog:list')


class BlogUpdateView(UpdateView):
    """Update существующей сущности"""
    model = Blog
    fields = ('body', 'preview',)

    # success_url = reverse_lazy('blog:list')

    def get_success_url(self):
        """Переопределен метод, для перенаправления на статью после обновления."""
        return reverse('blog:detail', args=[self.object.slug])


class BlogListView(ListView):
    """Просмотр всех сущностей модели"""
    model = Blog


class BlogDetailView(DetailView):
    """Просмотр одной сущности из модели"""
    model = Blog

    def get_object(self, queryset=None):
        """Переопределение метода для подсчета количества просмотров"""
        self.object = super().get_object(queryset)
        # Счетчик просмотров
        self.object.views_count += 1
        if self.object.views_count == 100:
            # Отправка письма при достижении счетчиком отметки 100
            send_mail(
                'Поздравляем!!!',
                'Поздравляем! Статья набрала более ста просмотров',
                '', # your email
                [''], # to@exampl.com
                fail_silently=False,
            )
        self.object.save()
        return self.object


class BlogDeleteView(DeleteView):
    """Удаление объекта"""
    model = Blog
    success_url = reverse_lazy('blog:list')


def toggle_activity(request, pk):
    """Функция для переключения статуса опубликованное/неопубликованное"""
    blog_item = get_object_or_404(Blog, pk=pk)
    if blog_item.is_publication:
        blog_item.is_publication = False
    else:
        blog_item.is_publication = True
    blog_item.save()
    return redirect(reverse('blog:list'))
