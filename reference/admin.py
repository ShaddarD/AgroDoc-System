from django.contrib import admin
from .models import LookupStatusCode, Terminal, Product, PowerOfAttorney


@admin.register(Terminal)
class TerminalAdmin(admin.ModelAdmin):
    list_display = ('terminal_code', 'terminal_name', 'address_ru', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('terminal_code', 'terminal_name')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_code', 'name_ru', 'hs_code_tnved', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('product_code', 'name_ru', 'hs_code_tnved')


@admin.register(PowerOfAttorney)
class PowerOfAttorneyAdmin(admin.ModelAdmin):
    list_display = ('poa_number', 'issue_date', 'expiry_date', 'status_code', 'is_active')
    list_filter = ('status_code', 'is_active')
    search_fields = ('poa_number',)
