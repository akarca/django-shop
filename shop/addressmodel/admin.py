#-*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from shop.addressmodel.models import City, Township, Address

#class ClientAdmin(ModelAdmin):
#    pass
#admin.site.register(Client, ClientAdmin)

class TownshipInline(admin.TabularInline):
    model = Township


class CityAdmin(ModelAdmin):
    inlines = [TownshipInline]


class TownshipAdmin(ModelAdmin):
    pass


class AddressAdmin(ModelAdmin):
    list_display = (
        'get_full_name', 'address', 'city', 'town',
        'user_shipping', 'user_billing')
    raw_id_fields = ('user_shipping', 'user_billing')


admin.site.register(Address, AddressAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Township, TownshipAdmin)