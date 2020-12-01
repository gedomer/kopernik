from rest_framework.generics import (ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView)

from .models import Order
from .serializers import (OrderCreateSerializer, OrderDetailSerializer,
                          OrderListSerializer, OrderUpdateSerializer)


class OrderListAPIView(ListCreateAPIView):

    def get_queryset(self):
        queryset = Order.objects.all()

        status = self.request.query_params.get('status')
        if status:
            queryset = queryset.filter(status=status)

        customer_id = self.request.query_params.get('customer_id')
        if customer_id:
            queryset = queryset.filter(customer_id=customer_id)

        return queryset

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return OrderListSerializer
        return OrderCreateSerializer


class OrderDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    lookup_field = 'uuid'

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return OrderUpdateSerializer
        return OrderDetailSerializer
