from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from catalog.models import Product
from .forms import ReviewForm
from .models import Review

@login_required
def upsert_review(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_active=True)
    existing = Review.objects.filter(product=product, user=request.user).first()

    if request.method == "POST":
        form = ReviewForm(request.POST, instance=existing)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.product = product
            obj.user = request.user
            obj.save()
    return redirect("product_detail", slug=product.slug)
