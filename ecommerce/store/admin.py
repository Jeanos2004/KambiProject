from django.contrib import admin
from .models import Cart, CartItem, User, Category, Product, DeliveryPerson, Notification

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Product)

admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(DeliveryPerson)
admin.site.register(Notification)
