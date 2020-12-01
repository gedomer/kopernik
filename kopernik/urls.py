from django.urls import path

from .views import OrderDetailAPIView, OrderListAPIView

urlpatterns = [
    path('orders/', OrderListAPIView.as_view(), name='order-list-api'),
    path('orders/<uuid:uuid>/', OrderDetailAPIView.as_view(), name='order-detail-api')
]
