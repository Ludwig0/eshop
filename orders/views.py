from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import redirect, render, get_object_or_404
from cart.cart import Cart
from catalog.models import Product
from .forms import CheckoutForm
from .models import Order, OrderItem

@login_required
def checkout(request):
    cart = Cart(request)
    if cart.total_qty() == 0:
        return redirect("cart_detail")

    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                order = form.save(commit=False)
                order.user = request.user
                order.status = Order.Status.PENDING
                order.save()

                # 锁库存（select_for_update）+ 校验 + 扣减
                for item in cart:
                    product = Product.objects.select_for_update().get(id=item["product"].id)
                    qty = item["qty"]
                    if product.stock < qty:
                        # 库存不足：回滚整个事务
                        raise ValueError(f"库存不足：{product.name}")
                    product.stock -= qty
                    product.save()

                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        unit_price=product.price,
                        quantity=qty,
                    )

                cart.clear()
            return redirect("order_detail", order_id=order.id)
    else:
        form = CheckoutForm()

    return render(request, "orders/checkout.html", {"cart": cart, "form": form})

@login_required
def my_orders(request):
    qs = request.user.orders.all().order_by("-created_at")
    return render(request, "orders/my_orders.html", {"orders": qs})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, "orders/order_detail.html", {"order": order})
