from django.conf import settings
from django.db import models

class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "待支付"
        PAID = "PAID", "已支付"
        SHIPPED = "SHIPPED", "已发货"
        COMPLETED = "COMPLETED", "已完成"
        CANCELED = "CANCELED", "已取消"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    full_name = models.CharField(max_length=120)
    phone = models.CharField(max_length=50)
    address = models.CharField(max_length=255)
    note = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order#{self.id} {self.user.username} {self.status}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey("catalog.Product", on_delete=models.PROTECT)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()

    def line_total(self):
        return self.unit_price * self.quantity
