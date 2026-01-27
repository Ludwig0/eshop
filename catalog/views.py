from django.core.paginator import Paginator
from django.db.models import Avg
from django.shortcuts import get_object_or_404, render
from .models import Category, Product
from reviews.forms import ReviewForm

def home(request):
    return product_list(request)

def product_list(request, category_slug=None):
    q = request.GET.get("q", "").strip()
    products = Product.objects.filter(is_active=True)

    category = None
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    if q:
        products = products.filter(name__icontains=q)

    products = products.order_by("-created_at")
    paginator = Paginator(products, 12)
    page = paginator.get_page(request.GET.get("page"))

    categories = Category.objects.all().order_by("name")
    return render(request, "catalog/product_list.html", {
        "page": page,
        "categories": categories,
        "category": category,
        "q": q,
    })

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    reviews_qs = product.reviews.select_related("user")
    avg_rating = reviews_qs.aggregate(avg=Avg("rating"))["avg"]

    form = None
    if request.user.is_authenticated:
        from reviews.models import Review
        existing = Review.objects.filter(product=product, user=request.user).first()
        form = ReviewForm(instance=existing)

    return render(request, "catalog/product_detail.html", {
        "product": product,
        "reviews": reviews_qs,
        "avg_rating": avg_rating,
        "review_form": form,
    })
