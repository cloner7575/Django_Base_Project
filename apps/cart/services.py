from __future__ import annotations

from django.db import transaction
from django.http import HttpRequest

from apps.cart.models import Cart, CartItem
from apps.catalog.models import ProductVariant


class CartError(Exception):
    """Raised when a cart mutation is invalid."""


def _ensure_session(request: HttpRequest) -> None:
    if not request.session.session_key:
        request.session.create()


def get_or_create_cart(request: HttpRequest) -> Cart:
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(
            user=request.user,
            defaults={"session_key": None},
        )
        return cart
    _ensure_session(request)
    cart, _ = Cart.objects.get_or_create(
        session_key=request.session.session_key,
        user=None,
    )
    return cart


def get_cart_items(cart: Cart) -> list[CartItem]:
    return list(
        cart.items.select_related(
            "variant__product__category",
            "variant__color",
        )
        .prefetch_related("variant__product__images")
        .all()
    )


def cart_count(request: HttpRequest) -> int:
    cart = get_or_create_cart(request)
    return sum(item.quantity for item in get_cart_items(cart))


def cart_subtotal(request: HttpRequest) -> int:
    return sum(item.line_total for item in get_cart_items(get_or_create_cart(request)))


def lines(request: HttpRequest) -> list[dict[str, object]]:
    result: list[dict[str, object]] = []
    for item in get_cart_items(get_or_create_cart(request)):
        result.append(
            {
                "item": item,
                "variant": item.variant,
                "product": item.variant.product,
                "quantity": item.quantity,
                "unit_price": item.unit_price,
                "line_total": item.line_total,
                "size": item.variant.size,
                "color_name": item.color_name or item.variant.color_name,
            }
        )
    return result


def _variant_image(variant: ProductVariant) -> str:
    product = variant.product
    if product.image:
        try:
            return product.image.url
        except ValueError:
            pass
    primary = next(
        (img for img in product.images.all() if img.is_primary),
        None,
    )
    if primary is None:
        primary = next(iter(product.images.all()), None)
    if primary is not None:
        return primary.file.url
    return ""


def serialize(request: HttpRequest) -> dict[str, object]:
    items = []
    for line in lines(request):
        product = line["product"]
        variant = line["variant"]
        items.append(
            {
                "id": variant.pk,  # type: ignore[union-attr]
                "variant_id": variant.pk,  # type: ignore[union-attr]
                "name": product.name,  # type: ignore[union-attr]
                "size": line["size"],
                "color": line["color_name"],
                "qty": line["quantity"],
                "quantity": line["quantity"],
                "unit_price": line["unit_price"],
                "line_total": line["line_total"],
                "url": product.get_absolute_url(),  # type: ignore[union-attr]
                "image": _variant_image(variant),  # type: ignore[arg-type]
            }
        )
    return {
        "ok": True,
        "items": items,
        "cart_count": sum(int(i["qty"]) for i in items),  # type: ignore[arg-type]
        "subtotal": sum(int(i["line_total"]) for i in items),  # type: ignore[arg-type]
    }


def add_item(request: HttpRequest, variant: ProductVariant, quantity: int = 1) -> None:
    if quantity < 1:
        raise CartError("تعداد باید حداقل ۱ باشد.")
    if not variant.product.is_active:
        raise CartError("این محصول موجود نیست.")
    if variant.stock < 1:
        raise CartError("این بسته موجود نیست.")
    cart = get_or_create_cart(request)
    color_name = variant.color_name
    item, created = CartItem.objects.get_or_create(
        cart=cart,
        variant=variant,
        defaults={"quantity": quantity, "color_name": color_name},
    )
    if not created:
        new_qty = item.quantity + quantity
        if new_qty > variant.stock:
            raise CartError("موجودی کافی نیست.")
        item.quantity = new_qty
        item.save(update_fields=["quantity", "updated_at"])
    elif quantity > variant.stock:
        item.delete()
        raise CartError("موجودی کافی نیست.")


def set_quantity(request: HttpRequest, variant: ProductVariant, quantity: int) -> None:
    cart = get_or_create_cart(request)
    if quantity <= 0:
        CartItem.objects.filter(cart=cart, variant=variant).delete()
        return
    if quantity > variant.stock:
        raise CartError("موجودی کافی نیست.")
    item, _ = CartItem.objects.get_or_create(
        cart=cart,
        variant=variant,
        defaults={"quantity": quantity, "color_name": variant.color_name},
    )
    item.quantity = quantity
    item.color_name = variant.color_name
    item.save(update_fields=["quantity", "color_name", "updated_at"])


def remove_item(request: HttpRequest, variant_id: int) -> None:
    cart = get_or_create_cart(request)
    CartItem.objects.filter(cart=cart, variant_id=variant_id).delete()


def clear_cart(request: HttpRequest) -> None:
    cart = get_or_create_cart(request)
    cart.items.all().delete()


def is_empty(request: HttpRequest) -> bool:
    return not get_cart_items(get_or_create_cart(request))


@transaction.atomic
def merge_guest_cart(request: HttpRequest) -> None:
    if not request.user.is_authenticated:
        return
    _ensure_session(request)
    session_key = request.session.session_key
    if not session_key:
        return
    guest_cart = Cart.objects.filter(session_key=session_key, user=None).first()
    if guest_cart is None:
        return
    user_cart, _ = Cart.objects.get_or_create(
        user=request.user,
        defaults={"session_key": None},
    )
    for guest_item in guest_cart.items.select_related("variant", "variant__color"):
        color_name = guest_item.color_name or guest_item.variant.color_name
        item, created = CartItem.objects.get_or_create(
            cart=user_cart,
            variant=guest_item.variant,
            defaults={
                "quantity": guest_item.quantity,
                "color_name": color_name,
            },
        )
        if not created:
            item.quantity = min(
                item.quantity + guest_item.quantity,
                guest_item.variant.stock,
            )
            item.save(update_fields=["quantity", "updated_at"])
    guest_cart.delete()
