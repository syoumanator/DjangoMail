from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from email_validator import EmailNotValidError, validate_email


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, forms.EmailField):
                field.widget.attrs.update({"class": "form-control", "type": "email"})
            elif isinstance(field, forms.ImageField):
                field.widget.attrs.update({"class": "form-control", "type": "file"})
            elif isinstance(field, forms.BooleanField):
                field.widget.attrs.update({"class": "form-check-input"})
            else:
                field.widget.attrs.update({"class": "form-control"})


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    email = forms.EmailField(
        required=True, help_text="Введите актуальный адрес электронной почты."
    )
    avatar = forms.ImageField(
        required=False, help_text="Необязательно. Загрузите изображение для аватарки."
    )
    phone_number = forms.CharField(
        max_length=15,
        required=False,
        help_text="Необязательно. Введите актуальный номер телефона.",
    )
    area = forms.CharField(
        max_length=15,
        required=False,
        help_text="Необязательно. Введите страну проживания.",
    )

    class Meta:
        model = CustomUser
        fields = ("email", "avatar", "phone_number", "area", "password1", "password2")

        def clean_email(self):
            email = self.cleaned_data.get("email")
            try:
                validate_email(email)
            except EmailNotValidError as e:
                raise forms.ValidationError(str(e))
            return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")
        if phone_number and not phone_number.isdigit():
            raise forms.ValidationError("Номер телефона должен содержать только цифры.")
        return phone_number


class UserEditForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ("email", "first_name", "last_name", "avatar", "phone_number", "area")
        exclude = ("password1", "password2")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            validate_email(email)
        except EmailNotValidError as e:
            raise forms.ValidationError(str(e))
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")
        if phone_number and not phone_number.isdigit():
            raise forms.ValidationError("Номер телефона должен содержать только цифры.")
        return phone_number


class UserManagerEditForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ("is_active",)
