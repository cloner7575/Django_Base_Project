from apps.cart import services as cart_services


def cart(request):  # type: ignore[no-untyped-def]
    return {
        "cart_count": cart_services.cart_count(request),
        "cart_subtotal": cart_services.cart_subtotal(request),
    }
