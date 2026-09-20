from django import forms
from django.utils.translation import gettext_lazy as _


class ContactForm(forms.Form):
    name = forms.CharField(
        label=_("Name"),
        max_length=120,
        widget=forms.TextInput(
            attrs={
                "autocomplete": "name",
                "placeholder": _("Your name"),
            }
        ),
    )
    email = forms.EmailField(
        label=_("Email"),
        widget=forms.EmailInput(
            attrs={
                "autocomplete": "email",
                "inputmode": "email",
                "placeholder": _("you@example.com"),
                "dir": "ltr",
                "class": "ltr",
            }
        ),
    )
    message = forms.CharField(
        label=_("Message"),
        max_length=5000,
        widget=forms.Textarea(
            attrs={
                "rows": 5,
                "placeholder": _("Tell me about the project or role."),
            }
        ),
    )
