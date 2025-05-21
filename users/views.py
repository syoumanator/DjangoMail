# from django.core.mail import send_mail
# from django.shortcuts import get_object_or_404, redirect
# from django.urls import reverse_lazy, reverse
# from django.views.generic import CreateView
# from .forms import CustomUserCreationForm
# import secrets
# from config.settings import EMAIL_HOST_USER
# from .models import CustomUser


# class RegisterView(CreateView):
#     form_class = CustomUserCreationForm
#     success_url = reverse_lazy('users:login')
#     template_name = 'users/register.html'
#
#     def form_valid(self, form):
#         user = form.save()
#         user.is_active = False
#         self.send_verification_email(user)
#         self.send_welcome_email(user.email)
#         return super().form_valid(form)
#
#     def send_welcome_email(self, user_email):
#         subject = 'Добро пожаловать'
#         message = 'Спасибо за регистрацию!'
#         from_email = EMAIL_HOST_USER
#         recipient_list = [user_email]
#         send_mail(subject, message, from_email, recipient_list)
#
#     def send_verification_email(self, user):
#         # Отправка подтверждения регистрации
#         token = secrets.token_hex(16)
#         user.verification_token = token
#         user.save()
#         host = self.request.get_host()
#         url = f'http://{host}/users/email-confirm/{token}/'
#         send_mail(
#             subject='Подтверждение регистрации',
#             message=f'Для подтверждения регистрации перейдите по ссылке: {url}',
#             from_email=EMAIL_HOST_USER,
#             recipient_list=[user.email, ]
#         )
#
#
# def email_verification(request, token):
#     user = get_object_or_404(CustomUser, verification_token=token)
#     user.is_active = True
#     user.save()
#     return redirect(reverse('users:login'))


from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView

from .forms import UserEditForm, UserManagerEditForm, UserRegisterForm
from .models import CustomUser
from .services import UserService


class UsersListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = CustomUser
    template_name = "users/user_list.html"
    permission_required = "users.can_view_user_list"
    context_object_name = "users"

    def get_queryset(self):
        return super().get_queryset().filter(is_staff=False)


class UserCreateView(CreateView):
    template_name = "users/register.html"
    form_class = UserRegisterForm
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        host = self.request.get_host()
        UserService.send_verification_email(user, host)
        return super().form_valid(form)


def email_verification(request, verification_token):
    user = get_object_or_404(CustomUser, verification_token=verification_token)
    user.is_active = True
    user.save()
    return redirect(reverse("users:login"))


class UserProfileUpdateView(UpdateView):
    model = CustomUser
    form_class = UserEditForm
    template_name = "users/profile_edit.html"
    login_url = reverse_lazy("users:login")
    success_url = reverse_lazy("users:profile_detail")
    context_object_name = "user"

    def get_success_url(self):
        return reverse("users:profile_detail", kwargs={"pk": self.kwargs["pk"]})

    def get_form_class(self):
        if self.request.user.has_perm("users.can_blocking_user"):
            return UserManagerEditForm
        else:
            return UserEditForm


@method_decorator(cache_page(60 * 5), name="dispatch")  # Cache for 5 minutes
class UserProfileDetailView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = "users/profile_detail.html"
    login_url = reverse_lazy("users:login")
    context_object_name = "user"
