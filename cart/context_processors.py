from .cart import Cart

def cart_summary(request):
    cart = Cart(request)
    return {"cart_total_qty": cart.total_qty()}
