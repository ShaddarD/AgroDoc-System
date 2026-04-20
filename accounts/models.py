import uuid
from django.db import models
from django.contrib.postgres.fields import ArrayField


class LookupRoleCode(models.Model):
    role_code = models.CharField(max_length=50, primary_key=True)
    display_name_ru = models.CharField(max_length=100)
    display_name_en = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'lookup_role_codes'

    def __str__(self):
        return self.display_name_ru


class Counterparty(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name_ru = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255, null=True, blank=True)
    inn = models.CharField(max_length=12, null=True, blank=True)
    kpp = models.CharField(max_length=9, null=True, blank=True)
    ogrn = models.CharField(max_length=15, null=True, blank=True)
    legal_address_ru = models.TextField(null=True, blank=True)
    actual_address_ru = models.TextField(null=True, blank=True)
    legal_address_en = models.TextField(null=True, blank=True)
    actual_address_en = models.TextField(null=True, blank=True)
    status_code = models.CharField(max_length=50, default='active')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'counterparties'

    def __str__(self):
        return self.name_ru


class Account(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    login = models.CharField(max_length=100, unique=True)
    password_hash = models.TextField()
    role_code = models.CharField(max_length=50)
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, null=True, blank=True)
    counterparty = models.ForeignKey(
        Counterparty, on_delete=models.SET_NULL, null=True, blank=True,
        db_column='counterparty_uuid', related_name='accounts',
    )
    phone = models.CharField(max_length=32, null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    job_title = models.CharField(max_length=150, null=True, blank=True)
    permissions = ArrayField(models.CharField(max_length=100), default=list, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'accounts'

    def __str__(self):
        return f'{self.last_name} {self.first_name} ({self.login})'

    @property
    def full_name(self):
        parts = [self.last_name, self.first_name]
        if self.middle_name:
            parts.append(self.middle_name)
        return ' '.join(parts)
