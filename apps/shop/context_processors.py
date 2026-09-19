from apps.shop.cart import Cart


def shop(request):  # type: ignore[no-untyped-def]
    cart = Cart(request)
    return {
        "cart_count": len(cart),
        "cart_subtotal": cart.total(),
    }
