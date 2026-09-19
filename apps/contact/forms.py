from __future__ import annotations

from django import forms

from apps.contact.models import ConsultationRequest


class ConsultationForm(forms.ModelForm):
    class Meta:
        model = ConsultationRequest
        fields = ("name", "phone", "email", "service_interest", "message")
        widgets = {
            "name": forms.TextInput(
                attrs={"autocomplete": "name", "placeholder": "نام و نام خانوادگی"}
            ),
            "phone": forms.TextInput(
                attrs={
                    "autocomplete": "tel",
                    "inputmode": "tel",
                    "dir": "ltr",
                    "placeholder": "0912…",
                }
            ),
            "email": forms.EmailInput(attrs={"autocomplete": "email", "dir": "ltr"}),
            "service_interest": forms.TextInput(
                attrs={"placeholder": "مثلاً تابلو نئون فروشگاه"}
            ),
            "message": forms.Textarea(attrs={"rows": 5}),
        }

    def clean_phone(self) -> str:
        phone = self.cleaned_data["phone"].strip().replace(" ", "")
        digits = phone.replace("+", "").replace("-", "")
        if not digits.isdigit() or len(digits) < 10:
            raise forms.ValidationError("شماره تماس معتبر وارد کنید.")
        return phone
