from django.contrib import admin

from . models import*
# Register your models here.
admin.site.register(Products)
admin.site.register(Color)
admin.site.register(Size)
admin.site.register(Tags)
admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(ShippingAddress)
admin.site.register(Cart)
admin.site.register(UserAddress)
admin.site.register(Coupon)
admin.site.register(OrderCart)
admin.site.register(Offer)
admin.site.register(CategoryOffer)
admin.site.register(ProductVariation)
