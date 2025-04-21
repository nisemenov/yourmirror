from django import forms
from .models import WishItemModel


class WishItemForm(forms.ModelForm):
    class Meta:
        model = WishItemModel
        fields = ["title", "link", "description", "picture", "is_private"]
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "w-full border border-gray-300 rounded-xl p-2"}
            ),
            "link": forms.URLInput(
                attrs={"class": "w-full border border-gray-300 rounded-xl p-2"}
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "w-full border border-gray-300 rounded-xl p-2",
                    "rows": 3,
                }
            ),
            "picture": forms.ClearableFileInput(
                attrs={"class": "w-full border border-gray-300 rounded-xl p-2"}
            ),
            "is_private": forms.CheckboxInput(attrs={"class": "mr-2"}),
        }

    def save(self, commit=True, profile=None):
        instance = super().save(commit=False)
        if profile:
            instance.profile = profile
        if commit:
            instance.save()
        return instance
