from __future__ import annotations

from django.http import HttpRequest

from apps.shop.models import ProductVariant

CART_SESSION_KEY = "shop_cart"


class CartError(Exception):
    """Raised when a cart mutation is invalid."""


class Cart:
    """Session-backed cart: {variant_id: quantity}."""

    def __init__(self, request: HttpRequest) -> None:
        self.session = request.session
        cart = self.session.get(CART_SESSION_KEY)
        if cart is None:
            cart = {}
            self.session[CART_SESSION_KEY] = cart
        # Legacy product_id carts are dropped when resolving lines().
        self._cart: dict[str, int] = {str(k): int(v) for k, v in cart.items()}

    @property
    def items(self) -> dict[str, int]:
        return self._cart

    @property
    def is_empty(self) -> bool:
        return not self._cart

    def __len__(self) -> int:
        return sum(self._cart.values())

    def add(self, variant: ProductVariant, quantity: int = 1) -> None:
        if quantity < 1:
            raise CartError("تعداد باید حداقل ۱ باشد.")
        if not variant.product.is_active:
            raise CartError("این محصول موجود نیست.")
        if variant.stock < 1:
            raise CartError("این بسته موجود نیست.")
        key = str(variant.pk)
        new_qty = self._cart.get(key, 0) + quantity
        if new_qty > variant.stock:
            raise CartError("موجودی کافی نیست.")
        self._cart[key] = new_qty
        self._save()

    def set_quantity(self, variant: ProductVariant, quantity: int) -> None:
        key = str(variant.pk)
        if quantity <= 0:
            self._cart.pop(key, None)
            self._save()
            return
        if quantity > variant.stock:
            raise CartError("موجودی کافی نیست.")
        self._cart[key] = quantity
        self._save()

    def remove(self, variant_id: int) -> None:
        self._cart.pop(str(variant_id), None)
        self._save()

    def clear(self) -> None:
        self._cart.clear()
        self._save()

    def _save(self) -> None:
        self.session[CART_SESSION_KEY] = self._cart
        if hasattr(self.session, "modified"):
            self.session.modified = True

    def lines(self) -> list[dict[str, object]]:
        variant_ids = [int(vid) for vid in self._cart]
        variants = {
            v.pk: v
            for v in ProductVariant.objects.filter(pk__in=variant_ids)
            .select_related("product", "product__category", "color")
            .prefetch_related("product__images")
        }
        result: list[dict[str, object]] = []
        stale: list[str] = []
        for vid_str, qty in self._cart.items():
            variant = variants.get(int(vid_str))
            if variant is None:
                stale.append(vid_str)
                continue
            unit = variant.effective_price
            result.append(
                {
                    "variant": variant,
                    "product": variant.product,
                    "quantity": qty,
                    "unit_price": unit,
                    "line_total": unit * qty,
                    "size": variant.size,
                    "color_name": variant.color_name,
                }
            )
        for key in stale:
            self._cart.pop(key, None)
        if stale:
            self._save()
        return result

    def total(self) -> int:
        return sum(int(line["line_total"]) for line in self.lines())

    def serialize(self) -> dict[str, object]:
        items = []
        for line in self.lines():
            product = line["product"]
            items.append(
                {
                    "variant_id": line["variant"].pk,  # type: ignore[union-attr]
                    "name": product.name,  # type: ignore[union-attr]
                    "size": line["size"],
                    "color": line["color_name"],
                    "quantity": line["quantity"],
                    "unit_price": line["unit_price"],
                    "line_total": line["line_total"],
                    "url": product.get_absolute_url(),  # type: ignore[union-attr]
                }
            )
        return {
            "items": items,
            "cart_count": len(self),
            "subtotal": self.total(),
        }
