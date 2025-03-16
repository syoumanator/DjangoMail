from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .forms import MailMessageForm, RecipientForm
from .models import RecipientMail, MailMessage


# ПОЛУЧАТЕЛИ
class RecipientMailListViews(LoginRequiredMixin, ListView):
    model = RecipientMail
    template_name = 'mailapp/recipient_mail_list.html'
    context_object_name = 'recipients'


class RecipientMailDetailViews(LoginRequiredMixin, DetailView):
    model = RecipientMail
    template_name = "mailapp/recipient_mail_detail.html"
    context_object_name = "recipient"


class RecipientMailCreateViews(LoginRequiredMixin, CreateView):
    model = RecipientMail
    form_class = RecipientForm
    context_object_name = "recipient"
    template_name = "mailapp/recipient_mail_form.html"
    success_url = reverse_lazy("mailapp:recipient_list")


class RecipientMailUpdateViews(LoginRequiredMixin, UpdateView):
    model = RecipientMail
    context_object_name = "recipient"
    template_name = "mailapp/recipient_mail_form.html"
    fields = ["email", "full_name", "comment"]
    success_url = reverse_lazy("mailapp:recipient_detail")

    def get_success_url(self):
        recipient = self.object
        return reverse_lazy("mailapp:recipient_detail", kwargs={"pk": recipient.pk})


class RecipientMailDeleteViews(LoginRequiredMixin, DeleteView):
    model = RecipientMail
    context_object_name = "recipient"
    template_name = "mailapp/recipient_mail_confirm_delete.html"
    success_url = reverse_lazy("mailapp:recipient_list")


# СООБЩЕНИЯ
class MailMessageListViews(LoginRequiredMixin, ListView):
    model = MailMessage
    template_name = "mailapp/mail_message_list.html"
    context_object_name = "messages"


class MailMessageDetailViews(LoginRequiredMixin, DetailView):
    model = MailMessage
    template_name = "mailapp/mail_message_detail.html"
    context_object_name = "message"


class MailMessageCreateViews(LoginRequiredMixin, CreateView):
    model = MailMessage
    template_name = "mailapp/mail_message_form.html"
    form_class = MailMessageForm
    success_url = reverse_lazy("mailapp:mail_message_list")




class MailMessageUpdateViews(LoginRequiredMixin, UpdateView):
    model = MailMessage
    context_object_name = "message"
    template_name = "mailapp/mail_message_form.html"
    form_class = MailMessageForm
    success_url = reverse_lazy("mailapp:message_detail")

    def get_success_url(self):
        message = self.object
        return reverse_lazy("mailapp:message_detail", kwargs={"pk": message.pk})


class MailMessageDeleteViews(DeleteView):
    model = MailMessage
    context_object_name = "message"
    template_name = "mailapp/mail_message_confirm_delete.html"
    success_url = reverse_lazy("mailapp:mail_message_list")
