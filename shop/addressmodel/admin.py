#-*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from shop.addressmodel.models import City, Town, Address

#class ClientAdmin(ModelAdmin):
#    pass
#admin.site.register(Client, ClientAdmin)


class CityAdmin(ModelAdmin):
    pass

class TownAdmin(ModelAdmin):
    pass


class AddressAdmin(ModelAdmin):
    list_display = (
        'name', 'address', 'address2', 'zip_code', 'city', 'country',
        'user_shipping', 'user_billing')
    raw_id_fields = ('user_shipping', 'user_billing')


admin.site.register(Address, AddressAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Town, TownAdmin)