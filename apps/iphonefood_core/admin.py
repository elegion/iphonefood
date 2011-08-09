from django.contrib import admin

from iphonefood_core.models import Menu, Category, Dish, Address


class DishAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'rating')


class AddressAdmin(admin.ModelAdmin):
    list_display = ('address', 'district', 'city')


admin.site.register(Menu)
admin.site.register(Category)
admin.site.register(Dish, DishAdmin)
admin.site.register(Address, AddressAdmin)