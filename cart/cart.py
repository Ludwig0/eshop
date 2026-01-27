from decimal import Decimal
from catalog.models import Product

class Cart:
    SESSION_KEY = "cart"

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(self.SESSION_KEY)
        if not cart:
            cart = self.session[self.SESSION_KEY] = {}
        self.cart = cart

    def add(self, product_id, qty=1, override=False):
        pid = str(product_id)
        if pid not in self.cart:
            self.cart[pid] = {"qty": 0}
        if override:
            self.cart[pid]["qty"] = int(qty)
        else:
            self.cart[pid]["qty"] += int(qty)
        self.save()

    def remove(self, product_id):
        pid = str(product_id)
        if pid in self.cart:
            del self.cart[pid]
            self.save()

    def clear(self):
        self.session[self.SESSION_KEY] = {}
        self.session.modified = True

    def save(self):
        self.session[self.SESSION_KEY] = self.cart
        self.session.modified = True

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids, is_active=True)
        product_map = {str(p.id): p for p in products}

        for pid, item in self.cart.items():
            p = product_map.get(pid)
            if not p:
                continue
            qty = item["qty"]
            yield {
                "product": p,
                "qty": qty,
                "line_total": (p.price * Decimal(qty)),
            }

    def total_qty(self):
        return sum(i["qty"] for i in self.cart.values())

    def total_price(self):
        total = Decimal("0.00")
        for x in self:
            total += x["line_total"]
        return total
