from typing import cast
from django import forms
from django.forms.widgets import ClearableFileInput

from profiles.models import ProfileModel

from .models import WishItemModel


BASE_INPUT_CLASS = (
    "w-full border-b-1 border-gray-300 outline-none caret-black focus:caret-black"
)


class CustomClearableFileInput(ClearableFileInput):
    template_name = "wishitem/widgets/custom_clearable_file_input.html"


class WishItemForm(forms.ModelForm):  # type: ignore[type-arg]
    class Meta:
        model = WishItemModel
        labels = {
            "title": "Название",
            "description": "Описание",
            "link": "Ссылка",
            "picture": "Изображение",
            "price": "Цена",
            "price_currency": "Валюта",
            "is_private": "сделать приватным",
        }
        exclude = [
            "id",
            "profile",
            "reserved",
            "reserved_at",
            "created_at",
            "updated_at",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": BASE_INPUT_CLASS}),
            "description": forms.Textarea(attrs={"rows": 2, "class": BASE_INPUT_CLASS}),
            "link": forms.URLInput(attrs={"class": BASE_INPUT_CLASS}),
            "picture": CustomClearableFileInput(attrs={"class": BASE_INPUT_CLASS}),
            "price": forms.TextInput(attrs={"class": BASE_INPUT_CLASS}),
            "price_currency": forms.Select(attrs={"class": BASE_INPUT_CLASS}),
            "is_private": forms.CheckboxInput(),
        }

    def save(
        self,
        commit: bool = True,
        profile: ProfileModel | None = None,
    ) -> WishItemModel:
        instance = super().save(commit=False)
        if profile:
            instance.profile = profile
        if commit:
            instance.save()
        return cast(WishItemModel, instance)


class EmailReserveForm(forms.Form):
    email = forms.EmailField(help_text="email")
