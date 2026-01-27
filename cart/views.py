from django.shortcuts import get_object_or_404, redirect, render
from catalog.models import Product
from .cart import Cart

def cart_detail(request):
    cart = Cart(request)
    return render(request, "cart/cart_detail.html", {"cart": cart})

def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id, is_active=True)
    qty = int(request.POST.get("qty", 1))
    cart.add(product.id, qty=qty, override=False)
    return redirect("cart_detail")

def cart_update(request, product_id):
    cart = Cart(request)
    qty = int(request.POST.get("qty", 1))
    cart.add(product_id, qty=qty, override=True)
    return redirect("cart_detail")

def cart_remove(request, product_id):
    cart = Cart(request)
    cart.remove(product_id)
    return redirect("cart_detail")

def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")
