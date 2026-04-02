from django.contrib import admin
from .models import (
    ApplicationStatus, SenderRu, SenderPowerOfAttorney, Receiver,
    Gost, TrTs, TrTsSampling, Product, ProductPurpose, PackingType,
    Country, Representative, SamplingPlace, Laboratory, Certificate, Regulation,
)


@admin.register(ApplicationStatus)
class ApplicationStatusAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'sort_order')
    search_fields = ('name', 'code')
    ordering = ('sort_order',)


class SenderPowerOfAttorneyInline(admin.TabularInline):
    model = SenderPowerOfAttorney
    extra = 0
    fields = ('number', 'date', 'valid_from', 'valid_to', 'is_active')


@admin.register(SenderRu)
class SenderRuAdmin(admin.ModelAdmin):
    list_display = ('name', 'inn', 'kpp', 'ogrn', 'is_active')
    list_filter = ('is_active',)
    list_editable = ('is_active',)
    search_fields = ('name', 'inn', 'ogrn')
    inlines = [SenderPowerOfAttorneyInline]


@admin.register(SenderPowerOfAttorney)
class SenderPowerOfAttorneyAdmin(admin.ModelAdmin):
    list_display = ('sender', 'number', 'date', 'valid_from', 'valid_to', 'is_active')
    list_filter = ('is_active', 'sender')
    search_fields = ('number', 'sender__name')


@admin.register(Receiver)
class ReceiverAdmin(admin.ModelAdmin):
    list_display = ('name_en', 'inn', 'is_active')
    list_filter = ('is_active',)
    list_editable = ('is_active',)
    search_fields = ('name_en', 'inn', 'ogrn')


@admin.register(Gost)
class GostAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')
    search_fields = ('code', 'name')


@admin.register(TrTs)
class TrTsAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')
    search_fields = ('code', 'name')


@admin.register(TrTsSampling)
class TrTsSamplingAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')
    search_fields = ('code', 'name')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name_ru', 'botanical_name', 'gost', 'tr_ts', 'is_active')
    list_filter = ('is_active',)
    list_editable = ('is_active',)
    search_fields = ('name_ru', 'botanical_name')


@admin.register(ProductPurpose)
class ProductPurposeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(PackingType)
class PackingTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name_ru', 'name_en', 'iso_code')
    search_fields = ('name_ru', 'name_en', 'iso_code')


@admin.register(Representative)
class RepresentativeAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'company_name', 'email', 'phone')
    search_fields = ('full_name', 'company_name', 'email')


@admin.register(SamplingPlace)
class SamplingPlaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'address')
    search_fields = ('name', 'address')


@admin.register(Laboratory)
class LaboratoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_name')
    search_fields = ('name', 'short_name')


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Regulation)
class RegulationAdmin(admin.ModelAdmin):
    list_display = ('name', 'regulation_type')
    list_filter = ('regulation_type',)
    search_fields = ('name', 'regulation_type')
