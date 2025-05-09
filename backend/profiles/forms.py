from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


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
