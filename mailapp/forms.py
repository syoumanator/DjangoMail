from django import forms

from .models import Mailing, MailMessage, RecipientMail


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, forms.BooleanField):
                field.widget.attrs.update({"class": "form-check-input"})
            else:
                field.widget.attrs.update({"class": "form-control"})


class RecipientForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = RecipientMail
        fields = ["email", "full_name", "comment"]


class MailingForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ["message", "recipients", "frequency"]


class MailMessageForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = MailMessage
        fields = ["subject", "body"]