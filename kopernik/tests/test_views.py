import uuid

from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from ..enums import OrderStatus, PizzaSize
from ..models import Order
from ..utils.factories import (CustomerFactory, OrderFactory, OrderItemFactory,
                               PizzaFactory)


class TestOrderListTestCase(TestCase):

    def setUp(self):
        super().setUp()
        self.path = reverse('order-list-api')
        self.customer = CustomerFactory()
        self.customer_2 = CustomerFactory()

        self.vegetarian = PizzaFactory(name='Vegetarian')
        self.salami = PizzaFactory(name='Salami')

    def test_get_order_list(self):
        OrderFactory(customer=self.customer, status=OrderStatus.DELIVERED)
        OrderFactory(customer=self.customer, status=OrderStatus.ON_THE_WAY)
        OrderFactory(customer=self.customer_2, status=OrderStatus.CANCELLED)

        response = self.client.get(self.path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

        # filter by customer
        path = f'{self.path}?customer_id={self.customer.pk}'
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        # filter by status
        path = f'{self.path}?status={OrderStatus.DELIVERED}'
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        # filter by status and customer
        path = f'{self.path}?status={OrderStatus.DELIVERED}&customer_id={self.customer.pk}'
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_order(self):
        payload = {
            'customer_id': self.customer.pk,
            'customer_address': 'John Doe 123 Main St Anytown, USA',
            'products': [
                {'pizza': self.vegetarian.id, 'quantity': 1, 'size': PizzaSize.MEGA},
                {'pizza': self.salami.id, 'quantity': 2, 'size': PizzaSize.SMALL},
            ]
        }
        response = self.client.post(self.path, payload, content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)

        order = Order.objects.first()
        self.assertEqual(order.orderitem_set.count(), 2)


class TestOrderDetailTestCase(TestCase):

    def setUp(self):
        super().setUp()
        self.customer = CustomerFactory()
        self.order = OrderFactory(customer=self.customer, status=OrderStatus.DELIVERED)
        self.path = reverse('order-detail-api', args=(self.order.pk,))

        self.vegetarian = PizzaFactory(name='Vegetarian')
        self.salami = PizzaFactory(name='Salami')
        self.vegan = PizzaFactory(name='Vegan')

    def test_retrieve_order_valid(self):
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)
        self.assertEqual(response.data['status'], self.order.status)
        self.assertEqual(response.data['status_text'], self.order.get_status_display())
        self.assertEqual(response.data['address'], self.order.address)
        self.assertEqual(len(response.data['customer']), 2)
        self.assertEqual(response.data['customer']['user_name'], self.customer.get_username())
        self.assertEqual(response.data['customer']['full_name'], self.customer.get_full_name())

    def test_retrieve_order_invalid(self):
        path = reverse('order-detail-api', args=(uuid.uuid4(),))  # non-exist order
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_remove_order_valid(self):
        self.assertEqual(Order.objects.count(), 1)
        response = self.client.delete(self.path)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Order.objects.count(), 0)

    def test_remove_order_invalid(self):
        self.assertEqual(Order.objects.count(), 1)
        path = reverse('order-detail-api', args=(uuid.uuid4(),))  # non-exist order
        response = self.client.delete(path)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Order.objects.count(), 1)

    def test_update_order_valid(self):
        self.order.status = OrderStatus.ON_THE_WAY
        self.order.save(update_fields=['status'])
        self.order.refresh_from_db()

        self.assertTrue(self.order.status not in OrderStatus.unchangeable_statuses())
        OrderItemFactory(pizza=self.vegetarian, quantity=1, size=PizzaSize.MEGA, order=self.order)
        OrderItemFactory(pizza=self.salami, quantity=2, size=PizzaSize.SMALL, order=self.order)

        payload = {
            'products': [
                {'pizza': self.vegan.id, 'quantity': 3, 'size': PizzaSize.SMALL},
                {'pizza': self.salami.id, 'quantity': 4, 'size': PizzaSize.LARGE},
            ]
        }

        response = self.client.put(self.path, payload, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        order_item = self.order.orderitem_set.first()
        self.assertEqual(order_item.pizza_id, payload['products'][0]['pizza'])
        self.assertEqual(order_item.quantity, payload['products'][0]['quantity'])
        self.assertEqual(order_item.size, payload['products'][0]['size'])

    def test_update_order_invalid(self):
        self.assertTrue(self.order.status in OrderStatus.unchangeable_statuses())
        OrderItemFactory(pizza=self.vegetarian, quantity=1, size=PizzaSize.MEGA, order=self.order)
        OrderItemFactory(pizza=self.salami, quantity=2, size=PizzaSize.SMALL, order=self.order)

        payload = {
            'products': [
                {'pizza': self.vegetarian.id, 'quantity': 1, 'size': PizzaSize.MEGA},
                {'pizza': self.salami.id, 'quantity': 2, 'size': PizzaSize.SMALL},
            ]
        }

        response = self.client.put(self.path, payload, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_order_status_valid(self):
        self.order.status = OrderStatus.ON_THE_WAY
        self.order.save(update_fields=['status'])

        payload = {
            'status': OrderStatus.RECEIVED
        }
        response = self.client.put(self.path, payload, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, payload['status'])

    def test_update_order_status_invalid(self):
        payload = {
            'status': OrderStatus.RECEIVED
        }
        response = self.client.put(self.path, payload, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.order.status = OrderStatus.CANCELLED
        self.order.save(update_fields=['status'])
        response = self.client.put(self.path, payload, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
