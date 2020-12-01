from django.contrib import admin

from kopernik.models import Customer, Order, Pizza, OrderItem


class DeleteNotAllowedModelAdmin(admin.ModelAdmin):

    def get_actions(self, request):
        actions = super().get_actions(request)

        if actions.get('delete_selected'):
            del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Customer)
class CustomerAdmin(DeleteNotAllowedModelAdmin, admin.ModelAdmin):
    pass


@admin.register(Pizza)
class PizzaAdmin(admin.ModelAdmin):
    pass


class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 0
    max_num = 3


@admin.register(Order)
class OrderAdmin(DeleteNotAllowedModelAdmin, admin.ModelAdmin):
    inlines = [
        OrderItemInline,
    ]
