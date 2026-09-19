from django import forms

from apps.catalog.models import ProductVariant


class AddToCartForm(forms.Form):
    variant_id = forms.IntegerField(widget=forms.HiddenInput, required=False)
    quantity = forms.IntegerField(
        label="تعداد",
        min_value=1,
        initial=1,
        widget=forms.NumberInput(attrs={"min": 1}),
    )
    size = forms.CharField(required=False)
    color = forms.CharField(required=False)

    def resolve_variant(self, product_id: int) -> ProductVariant:
        cleaned = self.cleaned_data
        variant_id = cleaned.get("variant_id")
        if variant_id:
            return ProductVariant.objects.select_related("product", "color").get(
                pk=variant_id,
                product_id=product_id,
            )
        size = (cleaned.get("size") or "").strip()
        color = (cleaned.get("color") or "").strip()
        qs = ProductVariant.objects.filter(product_id=product_id)
        if size:
            qs = qs.filter(size=size)
        if color:
            qs = qs.filter(color__name=color)
        else:
            qs = qs.filter(color__isnull=True)
        variant = qs.select_related("product", "color").first()
        if variant is None:
            raise forms.ValidationError("بسته انتخاب‌شده معتبر نیست.")
        return variant


class CartUpdateForm(forms.Form):
    quantity = forms.IntegerField(label="تعداد", min_value=0)


class CheckoutForm(forms.Form):
    full_name = forms.CharField(label="نام و نام خانوادگی", max_length=200)
    phone = forms.CharField(label="شماره تماس", max_length=20)
    address = forms.CharField(
        label="آدرس تحویل",
        widget=forms.Textarea(attrs={"rows": 3}),
    )
