# -*- coding: utf-8 -*-
"""
Holds all the information relevant to the client (addresses for instance)
"""
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

from django.conf import settings

BASE_ADDRESS_TEMPLATE = \
_("""
Name: %(name)s,
Address: %(address)s,
Zip-Code: %(zipcode)s,
City: %(city)s,
State: %(state)s,
Country: %(country)s
""")

ADDRESS_TEMPLATE = getattr(settings, 'SHOP_ADDRESS_TEMPLATE',
                           BASE_ADDRESS_TEMPLATE)


# class Country(models.Model):
#     name = models.CharField(max_length=255)

#     def __unicode__(self):
#         return u'%s' % self.name

#     class Meta(object):
#         verbose_name = _('Country')
#         verbose_name_plural = _('Countries')


class City(models.Model):
    name = models.CharField(max_length=128)
    weight = models.IntegerField(default=0)

    class Meta:
        ordering = ['weight']

    def __unicode__(self):
        return self.name


class Township(models.Model):
    city = models.ForeignKey(City, verbose_name=u"İl")
    name = models.CharField(max_length=128)
    weight = models.IntegerField(default=0)

    class Meta:
        ordering = ['weight']

    def __unicode__(self):
        return self.name


class BaseAddress(models.Model):
    first_name = models.CharField(max_length=50,
                                  verbose_name=u"Ad")
    last_name = models.CharField(max_length=50,
                                 verbose_name=u"Soyad")
    address = models.TextField(verbose_name=u"Adres")
    city = models.ForeignKey(City,
                             verbose_name=u"İl")
    town = models.ForeignKey(Township,
                             verbose_name=u"İlçe")
    postal_code = models.CharField(max_length=5,
                                   verbose_name=u"Posta Kodu",
                                   blank=True,
                                   null=True)
    phone = models.CharField(max_length=13,
                             verbose_name=u"Telefon",
                             null=True,
                             blank=True)
    id_number = models.CharField(max_length=11,
                                 verbose_name=u"TC Kimlik No",
                                 blank=True,
                                 null=True)
    tax_office = models.CharField(max_length=64,
                                  verbose_name=u"Vergi Dairesi",
                                  blank=True,
                                  null=True)
    tax_id_number = models.CharField(max_length=20,
                                     verbose_name=u"Vergi Numarası",
                                     blank=True,
                                     null=True)

    class Meta:
        abstract = True

    def as_text(self):
        return """
        %s
        %s %s
        %s / %s
        %s
        """ % (self.get_full_name(),
               self.address, self.postal_code,
               self.town, self.city,
               self.phone)

    def clone(self):
        new_kwargs = dict([(fld.name, getattr(self, fld.name)) for fld in self._meta.fields if fld.name != 'id'])
        return self.__class__.objects.create(**new_kwargs)

    def __unicode__(self):
        return u"%s - %s" % (self.get_full_name(), self.city.name)

    def get_full_name(self):
        return u"%s %s" % (self.first_name.strip(), self.last_name.strip())


class Address(BaseAddress):
    user_shipping = models.OneToOneField(User, related_name='shipping_address',
                                         blank=True, null=True)

    user_billing = models.OneToOneField(User, related_name='billing_address',
                                        blank=True, null=True)



# class Address(models.Model):
#     user_shipping = models.OneToOneField(User, related_name='shipping_address',
#                                          blank=True, null=True)
#     user_billing = models.OneToOneField(User, related_name='billing_address',
#                                         blank=True, null=True)

#     name = models.CharField(_('Name'), max_length=255)
#     address = models.CharField(_('Address'), max_length=255)
#     address2 = models.CharField(_('Address2'), max_length=255, blank=True)
#     zip_code = models.CharField(_('Zip Code'), max_length=20)
#     city = models.CharField(_('City'), max_length=20)
#     state = models.CharField(_('State'), max_length=255)
#     country = models.ForeignKey(Country, verbose_name=_('Country'), blank=True,
#                                 null=True)

#     class Meta(object):
#         verbose_name = _('Address')
#         verbose_name_plural = _("Addresses")

#     def __unicode__(self):
#         return '%s (%s, %s)' % (self.name, self.zip_code, self.city)

#     def clone(self):
#         new_kwargs = dict([(fld.name, getattr(self, fld.name))
#                            for fld in self._meta.fields if fld.name != 'id'])
#         return self.__class__.objects.create(**new_kwargs)

#     def as_text(self):
#         return ADDRESS_TEMPLATE % {
#             'name': self.name,
#             'address': '%s\n%s' % (self.address, self.address2),
#             'zipcode': self.zip_code,
#             'city': self.city,
#             'state': self.state,
#             'country': self.country,
#         }