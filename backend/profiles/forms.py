from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import Q


class EmailRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:  # pyright: ignore
        model = User
        fields = (
            "email",
            "first_name",
            "password1",
            "password2",
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class UserSettingsForm(forms.ModelForm):
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

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)
        # self.fields["telegram_id"].initial = getattr(self.user.profile, "telegram_id", "")

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(Q(email=email) & ~Q(pk=self.user.pk)).exists():
            raise forms.ValidationError("Пользователь с таким email уже существует")
        return email

    def clean(self):
        cleaned_data = super().clean()
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

    def save(self, commit=True):
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
        return user
