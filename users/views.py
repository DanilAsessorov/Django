from django.shortcuts import render, redirect
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.conf import settings
from .forms import UserRegistrationForm, UserLoginForm
from .models import User


class UserRegistrationView(CreateView):
    """Регистрация пользователя"""
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        """Отправка приветственного письма после регистрации"""
        response = super().form_valid(form)

        # Автоматический вход после регистрации
        user = form.save()
        login(self.request, user)

        # Отправка приветственного письма
        subject = 'Добро пожаловать в наш магазин!'
        message = f'Здравствуйте, {user.email}!\n\nСпасибо за регистрацию в нашем интернет-магазине.'
        from_email = settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@example.com'
        recipient_list = [user.email]

        try:
            send_mail(subject, message, from_email, recipient_list)
        except Exception as e:
            # Логируем ошибку, но не прерываем регистрацию
            print(f"Ошибка отправки письма: {e}")

        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация'
        return context


class UserLoginView(LoginView):
    """Авторизация пользователя"""
    form_class = UserLoginForm
    template_name = 'users/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Вход в аккаунт'
        return context


class UserLogoutView(LogoutView):
    """Выход из аккаунта"""
    next_page = reverse_lazy('home')


class ProfileView(TemplateView):
    """Профиль пользователя"""
    template_name = 'users/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context