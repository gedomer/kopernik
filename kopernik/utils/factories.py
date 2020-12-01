from django.conf import settings
from factory import Sequence, SubFactory
from factory.django import DjangoModelFactory
from kopernik.enums import PizzaSize


class UserFactory(DjangoModelFactory):
    username = Sequence(lambda n: "testuser%d" % n)
    first_name = Sequence(lambda n: "first_name%d" % n)
    last_name = Sequence(lambda n: "last_name%d" % n)
    email = Sequence(lambda n: "test-%d@kopernik.pizza" % n)

    class Meta:
        model = settings.AUTH_USER_MODEL


class CustomerFactory(DjangoModelFactory):
    user = SubFactory(UserFactory)

    class Meta:
        model = 'kopernik.Customer'


class PizzaFactory(DjangoModelFactory):

    class Meta:
        model = 'kopernik.Pizza'


class OrderFactory(DjangoModelFactory):

    class Meta:
        model = 'kopernik.Order'


class OrderItemFactory(DjangoModelFactory):
    order = SubFactory(OrderFactory)
    pizza = SubFactory(PizzaFactory)
    size = PizzaSize.LARGE
    quantity = 1

    class Meta:
        model = 'kopernik.OrderItem'
