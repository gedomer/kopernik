from django.utils.translation import gettext_lazy as _


class PizzaSize:
    SMALL = 1
    MEDIUM = 2
    LARGE = 3
    MEGA = 4

    AS_CHOICES = (
        (SMALL, _('Small')),
        (MEDIUM, _('Medium')),
        (LARGE, _('Large')),
        (MEGA, _('Mega')),
    )


class OrderStatus:
    CANCELLED = 'cancelled'
    RECEIVED = 'received'
    ON_THE_WAY = 'on-the-way'
    DELIVERED = 'delivered'

    AS_CHOICES = (
        (CANCELLED, _('Cancelled')),
        (RECEIVED, _('Received')),
        (ON_THE_WAY, _('On the way')),
        (DELIVERED, _('Delivered')),
    )

    @classmethod
    def unchangeable_statuses(cls):
        return [
            cls.CANCELLED,
            cls.DELIVERED
        ]
