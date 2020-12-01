import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from ..enums import OrderStatus
from .customer import Customer


class Order(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    status = models.CharField(choices=OrderStatus.AS_CHOICES, max_length=20)
    address = models.TextField(max_length=1000)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")
