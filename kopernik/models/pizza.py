from django.db import models
from django.utils.translation import gettext_lazy as _


class Pizza(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = _("Pizza")
        verbose_name_plural = _("Pizzas")

    def __str__(self):
        return self.name
