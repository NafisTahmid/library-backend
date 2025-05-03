from django.contrib import admin
from .models import Book, Review, Order, OrderItem, ShippingAddress, WishList

# Register your models here.
admin.site.register(Book),
admin.site.register(Review),
admin.site.register(Order),
admin.site.register(OrderItem),
admin.site.register(ShippingAddress),
admin.site.register(WishList)