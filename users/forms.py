from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User


AUTH_FIELD_CLASS = "block w-full border-b border-black outline-none py-3 mt-2 text-base"


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        label="email",
        label_suffix="",
        widget=forms.EmailInput(
            attrs={
                "class": AUTH_FIELD_CLASS,
                "id": "id_username",
                "required": "required",
            }
        ),
    )
    password = forms.CharField(
        label="Пароль",
        label_suffix="",
        widget=forms.PasswordInput(
            attrs={
                "class": AUTH_FIELD_CLASS,
                "id": "id_password",
                "required": "required",
            }
        ),
    )
    remember_me = forms.BooleanField(required=False, widget=forms.CheckboxInput())


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={
                "class": AUTH_FIELD_CLASS,
                "id": "id_email",
                "required": "required",
            }
        ),
        label="email",
        label_suffix="",
    )
    password1 = forms.CharField(
        label="Пароль",
        label_suffix="",
        widget=forms.PasswordInput(
            attrs={
                "class": AUTH_FIELD_CLASS,
                "id": "id_password1",
                "required": "required",
            }
        ),
    )
    password2 = forms.CharField(
        label="Подтверждение пароля",
        label_suffix="",
        widget=forms.PasswordInput(
            attrs={
                "class": AUTH_FIELD_CLASS,
                "id": "id_password2",
                "required": "required",
            }
        ),
    )

    class Meta:
        model = User
        fields = ("email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Этот email уже зарегистрирован.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data["email"]
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
