from django.db import models
from django.utils.translation import gettext_lazy as _
from kopernik.enums import PizzaSize

from .order import Order
from .pizza import Pizza


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    size = models.PositiveIntegerField(choices=PizzaSize.AS_CHOICES)
    quantity = models.PositiveIntegerField()

    class Meta:
        verbose_name = _("Order Item")
        verbose_name_plural = _("Order Items")
