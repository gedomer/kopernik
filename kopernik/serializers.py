from django.db import transaction
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from .enums import OrderStatus
from .models import Customer, Order, OrderItem


class CustomerSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        fields = ['user_name', 'full_name']

    def get_user_name(self, obj):
        return obj.get_username()

    def get_full_name(self, obj):
        return obj.get_full_name()


class OrderListSerializer(serializers.ModelSerializer):
    status_text = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['uuid', 'customer', 'status', 'address', 'status_text']

    def get_status_text(self, obj):
        return obj.get_status_display()


class OrderDetailSerializer(serializers.ModelSerializer):
    status_text = serializers.SerializerMethodField()
    customer = CustomerSerializer()

    class Meta:
        model = Order
        fields = ['status', 'status_text', 'address', 'customer']

    def get_status_text(self, obj):
        return obj.get_status_display()


class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = ['pizza', 'quantity', 'size']


class OrderUpdateSerializer(serializers.Serializer):
    products = OrderItemSerializer(many=True, write_only=True, required=False)
    status = serializers.ChoiceField(choices=OrderStatus.AS_CHOICES, required=False, write_only=True)

    def validate(self, data):
        data = super().validate(data)
        if self.instance.status in OrderStatus.unchangeable_statuses():
            raise serializers.ValidationError(_('Order can not be updated.'))
        return data

    def update(self, instance, validated_data):
        with transaction.atomic():
            if validated_data.get('products'):
                instance.orderitem_set.all().delete()
                order_items = []
                for product in validated_data.get('products'):
                    product.setdefault('order_id', instance.pk)
                    order_items.append(OrderItem(**product))
                OrderItem.objects.bulk_create(order_items)
            if validated_data.get('status') is not None:
                instance.status = validated_data['status']
                instance.save(update_fields=['status'])
        return instance


class OrderCreateSerializer(serializers.Serializer):
    customer_id = serializers.IntegerField(min_value=1, write_only=True)
    customer_address = serializers.CharField(write_only=True)
    products = OrderItemSerializer(many=True, write_only=True)

    def create(self, validated_data):
        with transaction.atomic():
            order = Order.objects.create(
                customer_id=validated_data['customer_id'],
                address=validated_data['customer_address']
            )
            order_items = []
            for product in validated_data['products']:
                product.setdefault('order_id', order.pk)
                order_items.append(OrderItem(**product))
            OrderItem.objects.bulk_create(order_items)
        return order
