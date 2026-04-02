import uuid
from django.db import models


class ApplicationStatus(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.TextField(unique=True)
    name = models.TextField()
    sort_order = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'dict_application_statuses'
        verbose_name = 'Статус заявки'
        verbose_name_plural = 'Статусы заявок'
        ordering = ['sort_order']

    def __str__(self):
        return self.name


class SenderRu(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.TextField()
    legal_address = models.TextField()
    actual_address = models.TextField()
    inn = models.TextField()
    kpp = models.TextField()
    ogrn = models.TextField()
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'dict_senders_ru'
        verbose_name = 'Отправитель (рус)'
        verbose_name_plural = 'Отправители (рус)'

    def __str__(self):
        return self.name


class SenderPowerOfAttorney(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(SenderRu, on_delete=models.CASCADE, related_name='powers_of_attorney')
    number = models.TextField()
    date = models.DateField()
    valid_from = models.DateField(null=True, blank=True)
    valid_to = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'sender_powers_of_attorney'
        verbose_name = 'Доверенность'
        verbose_name_plural = 'Доверенности'

    def __str__(self):
        return f"Дов. №{self.number} от {self.date}"


class Receiver(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name_en = models.TextField()
    legal_address = models.TextField()
    actual_address = models.TextField()
    inn = models.TextField(blank=True)
    kpp = models.TextField(blank=True)
    ogrn = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'dict_receivers'
        verbose_name = 'Получатель'
        verbose_name_plural = 'Получатели'

    def __str__(self):
        return self.name_en


class Gost(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.TextField()
    name = models.TextField()

    class Meta:
        db_table = 'dict_gosts'
        verbose_name = 'ГОСТ'
        verbose_name_plural = 'ГОСТы'

    def __str__(self):
        return f"{self.code} {self.name}"


class TrTs(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.TextField()
    name = models.TextField()

    class Meta:
        db_table = 'dict_tr_ts'
        verbose_name = 'ТР ТС'
        verbose_name_plural = 'ТР ТС'

    def __str__(self):
        return f"{self.code} {self.name}"


class TrTsSampling(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.TextField()
    name = models.TextField()

    class Meta:
        db_table = 'dict_tr_ts_sampling'
        verbose_name = 'ТР ТС (отбор)'
        verbose_name_plural = 'ТР ТС (отбор)'

    def __str__(self):
        return f"{self.code} {self.name}"


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name_ru = models.TextField()
    botanical_name = models.TextField(blank=True)
    gost = models.ForeignKey(Gost, on_delete=models.SET_NULL, null=True, blank=True)
    tr_ts = models.ForeignKey(TrTs, on_delete=models.SET_NULL, null=True, blank=True)
    tr_ts_sampling = models.ForeignKey(TrTsSampling, on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'dict_products'
        verbose_name = 'Продукция'
        verbose_name_plural = 'Продукция'

    def __str__(self):
        return self.name_ru


class ProductPurpose(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.TextField()

    class Meta:
        db_table = 'dict_product_purposes'
        verbose_name = 'Назначение продукции'
        verbose_name_plural = 'Назначения продукции'

    def __str__(self):
        return self.name


class PackingType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.TextField()

    class Meta:
        db_table = 'dict_packing_types'
        verbose_name = 'Тип упаковки'
        verbose_name_plural = 'Типы упаковки'

    def __str__(self):
        return self.name


class Country(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name_ru = models.TextField()
    name_en = models.TextField()
    iso_code = models.TextField(blank=True)

    class Meta:
        db_table = 'dict_countries'
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'

    def __str__(self):
        return self.name_ru


class Representative(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.TextField()
    email = models.TextField()
    phone = models.TextField()
    company_name = models.TextField()

    class Meta:
        db_table = 'dict_representatives'
        verbose_name = 'Представитель'
        verbose_name_plural = 'Представители'

    def __str__(self):
        return self.full_name


class SamplingPlace(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.TextField()
    address = models.TextField(blank=True)

    class Meta:
        db_table = 'dict_sampling_places'
        verbose_name = 'Место отбора'
        verbose_name_plural = 'Места отбора'

    def __str__(self):
        return self.name


class Laboratory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.TextField()
    short_name = models.TextField(blank=True)

    class Meta:
        db_table = 'dict_laboratories'
        verbose_name = 'Лаборатория'
        verbose_name_plural = 'Лаборатории'

    def __str__(self):
        return self.short_name or self.name


class Certificate(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.TextField()

    class Meta:
        db_table = 'dict_certificates'
        verbose_name = 'Сертификат'
        verbose_name_plural = 'Сертификаты'

    def __str__(self):
        return self.name


class Regulation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.TextField()
    regulation_type = models.TextField(blank=True)

    class Meta:
        db_table = 'dict_regulations'
        verbose_name = 'Регламент'
        verbose_name_plural = 'Регламенты'

    def __str__(self):
        return self.name
