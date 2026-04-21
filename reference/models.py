import uuid
from django.db import models
from accounts.models import Counterparty


class LookupStatusCode(models.Model):
    status_code = models.CharField(max_length=50, primary_key=True)
    description = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'lookup_status_codes'

    def __str__(self):
        return self.status_code


class Terminal(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    terminal_code = models.CharField(max_length=50, unique=True)
    terminal_name = models.CharField(max_length=255)
    owner_counterparty = models.ForeignKey(
        Counterparty, on_delete=models.SET_NULL, null=True, blank=True,
        db_column='owner_counterparty_uuid', related_name='owned_terminals',
    )
    address_ru = models.TextField()
    address_en = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'terminals'

    def __str__(self):
        return self.terminal_name


class Product(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product_code = models.CharField(max_length=50, unique=True)
    hs_code_tnved = models.CharField(max_length=20)
    name_ru = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255, null=True, blank=True)
    botanical_name_latin = models.CharField(max_length=255, null=True, blank=True)
    regulatory_documents = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'products'

    def __str__(self):
        return f'{self.product_code} — {self.name_ru}'


class PowerOfAttorney(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    poa_number = models.CharField(max_length=100)
    issue_date = models.DateField()
    validity_years = models.IntegerField()
    expiry_date = models.DateField(null=True, blank=True)  # GENERATED ALWAYS AS in DB
    principal_counterparty = models.ForeignKey(
        Counterparty, on_delete=models.RESTRICT, null=True, blank=True,
        db_column='principal_counterparty_uuid', related_name='poa_as_principal',
    )
    attorney_counterparty = models.ForeignKey(
        Counterparty, on_delete=models.RESTRICT, null=True, blank=True,
        db_column='attorney_counterparty_uuid', related_name='poa_as_attorney',
    )
    status_code = models.CharField(max_length=50, default='active')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'powers_of_attorney'

    def __str__(self):
        return f'Дов. №{self.poa_number} от {self.issue_date}'

    def _do_insert(self, manager, using, fields, returning_fields, raw):
        # expiry_date is GENERATED ALWAYS AS — PostgreSQL rejects any explicit value
        fields = [f for f in fields if f.attname != 'expiry_date']
        return super()._do_insert(manager, using, fields, returning_fields, raw)

    def _do_update(self, base_qs, using, pk_val, values, update_fields, forced_update):
        values = [(f, m, v) for f, m, v in values if f.attname != 'expiry_date']
        return super()._do_update(base_qs, using, pk_val, values, update_fields, forced_update)
