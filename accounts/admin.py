from django.contrib import admin
from .models import Counterparty, Account


@admin.register(Counterparty)
class CounterpartyAdmin(admin.ModelAdmin):
    list_display = ('name_ru', 'inn', 'kpp', 'status_code', 'is_active')
    list_filter = ('is_active', 'status_code')
    search_fields = ('name_ru', 'inn', 'ogrn')


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('login', 'last_name', 'first_name', 'role_code', 'is_active')
    list_filter = ('role_code', 'is_active')
    search_fields = ('login', 'last_name', 'first_name', 'email')
    exclude = ('password_hash',)
