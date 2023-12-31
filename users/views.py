import random

from django.conf import settings
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView

from users.forms import UserRegisterForm, UserUpdateForm
from users.models import User


class LoginView(BaseLoginView):
    template_name = 'users/login.html'


class LogoutView(BaseLogoutView):
    pass


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = "users/register.html"

    def form_valid(self, form):
        self.object = form.save()
        send_mail(
            subject='Поздравляем с успешной регистрацией!',
            message=f'Для успешного завершения регистрации введите на сайте VerificationCode {self.object.code}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.object.email]
        )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('users:mail_verification', kwargs={'pk': self.object.pk})


class UserUpdateView(UpdateView):
    model = User
    form_class = UserUpdateForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


def generate_new_password(request):
    new_password = ''.join([str(random.randint(0, 9)) for _ in range(10)])
    send_mail(
        subject='Сброс пароля',
        message=f'Ваш новый пароль - {new_password}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[request.user.email]
    )
    request.user.set_password(new_password)
    request.user.save()
    return redirect(reverse('catalog:products'))


def mail_verification(request, pk):
    user = User.objects.get(pk=pk)
    if request.method == 'POST':
        code = request.POST.get('code')
        if code == user.code:
            user.is_active = True
            user.save()
            return redirect(reverse('catalog:products'))
        else:
            raise ValueError('Неправильно введен код')
    return render(request, 'users/verification.html')
