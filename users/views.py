from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView
from .forms import CustomUserCreationForm
import secrets
from config.settings import EMAIL_HOST_USER
from .models import CustomUser


class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/register.html'

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        self.send_verification_email(user)
        self.send_welcome_email(user.email)
        return super().form_valid(form)

    def send_welcome_email(self, user_email):
        subject = 'Добро пожаловать'
        message = 'Спасибо за регистрацию!'
        from_email = EMAIL_HOST_USER
        recipient_list = [user_email]
        send_mail(subject, message, from_email, recipient_list)

    def send_verification_email(self, user):
        # Отправка подтверждения регистрации
        token = secrets.token_hex(16)
        user.verification_token = token
        user.save()
        host = self.request.get_host()
        url = f'http://{host}/users/email-confirm/{token}/'
        send_mail(
            subject='Подтверждение регистрации',
            message=f'Для подтверждения регистрации перейдите по ссылке: {url}',
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email, ]
        )


def email_verification(request, token):
    user = get_object_or_404(CustomUser, verification_token=token)
    user.is_active = True
    user.save()
    return redirect(reverse('users:login'))
