from typing import Any, cast

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import Q


class EmailRegistrationForm(UserCreationForm):  # type: ignore[type-arg]
    email = forms.EmailField(required=True)

    class Meta:  # pyright: ignore
        model = User
        fields = (
            "email",
            "first_name",
            "password1",
            "password2",
        )

    def save(self, commit: bool = True) -> User:
        user = super().save(commit=False)
        user.username = self.cleaned_data["email"]
        if commit:
            user.save()
        return cast(User, user)


class UserSettingsForm(forms.ModelForm):  # type: ignore[type-arg]
    email = forms.EmailField(required=True)
    # telegram_id = forms.CharField(required=False)

    current_password = forms.CharField(
        required=False, widget=forms.PasswordInput, label="Текущий пароль"
    )
    new_password1 = forms.CharField(
        required=False, widget=forms.PasswordInput, label="Новый пароль"
    )
    new_password2 = forms.CharField(
        required=False, widget=forms.PasswordInput, label="Повторите пароль"
    )

    class Meta:
        model = User
        fields = ("email", "first_name")

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)
        # self.fields["telegram_id"].initial = getattr(self.user.profile, "telegram_id", "")

    def clean_email(self) -> str:
        email = self.cleaned_data["email"]
        if User.objects.filter(Q(email=email) & ~Q(pk=self.user.pk)).exists():
            raise forms.ValidationError("Пользователь с таким email уже существует")
        return cast(str, email)

    def clean(self) -> dict[str, Any]:
        cleaned_data = super().clean() or {}
        p1 = cleaned_data.get("new_password1")
        p2 = cleaned_data.get("new_password2")
        if p1 or p2:
            if not cleaned_data.get("current_password"):
                self.add_error("current_password", "Укажите текущий пароль")
            elif not self.user.check_password(cleaned_data["current_password"]):
                self.add_error("current_password", "Неверный текущий пароль")
            if p1 != p2:
                self.add_error("new_password2", "Пароли не совпадают")
        return cleaned_data

    def save(self, commit: bool = True) -> User:
        user = self.user
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.username = self.cleaned_data["email"]
        if self.cleaned_data.get("new_password1"):
            user.set_password(self.cleaned_data["new_password1"])
        if commit:
            user.save()
            # user.profile.telegram_id = self.cleaned_data["telegram_id"]
            # user.profile.save()
        return cast(User, user)
