import uuid
from django.db import models


class Application(models.Model):
    TYPE_VNIIKR = 'vnikkr'
    TYPE_COK_SINGLE = 'cok_single'
    TYPE_COK_SPLIT = 'cok_split'

    TYPE_CHOICES = [
        (TYPE_VNIIKR, 'ВНИИКР'),
        (TYPE_COK_SINGLE, 'Одна заявка ЦОК АПК'),
        (TYPE_COK_SPLIT, 'Заявка в ЦОК АПК с разбивкой'),
    ]

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    application_number = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        unique=True,
    )

    application_type_code = models.CharField(
        max_length=50,
        choices=TYPE_CHOICES,
        default=TYPE_VNIIKR,
    )

    applicant_counterparty = models.ForeignKey(
        'accounts.Counterparty',
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        db_column='applicant_counterparty_uuid',
        related_name='applications_as_applicant',
        to_field='uuid',
    )
    applicant_account = models.ForeignKey(
        'accounts.Account',
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        db_column='applicant_account_uuid',
        related_name='applications_as_applicant',
        to_field='uuid',
    )
    terminal = models.ForeignKey(
        'reference.Terminal',
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        db_column='terminal_uuid',
        related_name='applications',
        to_field='uuid',
    )
    product = models.ForeignKey(
        'reference.Product',
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        db_column='product_uuid',
        related_name='applications',
        to_field='uuid',
    )
    power_of_attorney = models.ForeignKey(
        'reference.PowerOfAttorney',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='power_of_attorney_uuid',
        related_name='applications',
        to_field='uuid',
    )

    status = models.ForeignKey(
        'reference.LookupStatusCode',
        on_delete=models.RESTRICT,
        db_column='status_code',
        to_field='status_code',
        null=True,
        blank=True,
        related_name='applications',
    )

    master_application = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='master_application_uuid',
        related_name='child_applications',
        to_field='uuid',
    )

    stuffing_act_uuid = models.UUIDField(null=True, blank=True, db_index=True)

    sender_en_manual = models.TextField(null=True, blank=True)
    product_name_en_manual = models.TextField(null=True, blank=True)

    contract_number_manual = models.TextField(null=True, blank=True)
    contract_date_manual = models.DateField(null=True, blank=True)

    discharge_port_ru_manual = models.TextField(null=True, blank=True)
    discharge_port_en_manual = models.TextField(null=True, blank=True)

    additional_declaration = models.TextField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    harvest_year = models.IntegerField(null=True, blank=True)
    manufacture_date = models.DateField(null=True, blank=True)

    weight_mt = models.DecimalField(
        max_digits=14,
        decimal_places=3,
        null=True,
        blank=True,
    )

    planned_inspection_date = models.DateField(null=True, blank=True)
    planned_inspection_time = models.TimeField(null=True, blank=True)

    ikr_number = models.TextField(null=True, blank=True)
    ikr_date = models.DateField(null=True, blank=True)
    asid_number = models.TextField(null=True, blank=True)

    is_on_behalf = models.BooleanField(default=False)
    need_color_letter = models.BooleanField(default=False)

    submitted_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'applications'
        ordering = ['-created_at']

    def __str__(self):
        return f'Заявка {self.application_number or self.uuid}'


class InspectionRecord(models.Model):
    CARGO_STATUS_CHOICES = [
        ('waiting', 'Ожидает'),
        ('loaded', 'Погружен'),
        ('shipped', 'Отгружен'),
        ('on_way', 'В пути'),
        ('delivered', 'Доставлен'),
    ]

    DOC_STATUS_CHOICES = [
        ('not_ready', 'Не готовы'),
        ('in_progress', 'В процессе'),
        ('ready', 'Готовы'),
        ('issued', 'Выданы'),
    ]

    QUARANTINE_CHOICES = [
        ('own', 'Свои'),
        ('client', 'Клиентские'),
        ('shared', 'Совместные'),
        ('other', 'Другое'),
    ]

    id = models.BigAutoField(primary_key=True)

    number = models.CharField('№', max_length=100, blank=True)
    client = models.CharField('Клиент', max_length=300, blank=True)
    manager = models.CharField('Менеджер', max_length=200, blank=True)
    commodity = models.CharField('Культура', max_length=200, blank=True)
    container_count = models.TextField('Номера контейнеров', blank=True)
    container_type = models.CharField(
        'Тип контейнера',
        max_length=5,
        blank=True,
        choices=[('x20', 'x20'), ('x40', 'x40')],
    )
    weight = models.DecimalField('Вес (кг)', max_digits=12, decimal_places=2, null=True, blank=True)
    pod = models.CharField('POD', max_length=200, blank=True)
    terminal = models.CharField('Терминал', max_length=200, blank=True)
    quarantine = models.CharField(
        'Карантинки',
        max_length=50,
        choices=QUARANTINE_CHOICES,
        blank=True,
    )
    inspection_date_plan = models.DateField('ДОСМОТР (ПЛАН)', null=True, blank=True)
    fss_date_plan = models.DateField('Дата выдачи ФСС (ПЛАН)', null=True, blank=True)
    cargo_status = models.CharField(
        'Груз',
        max_length=50,
        choices=CARGO_STATUS_CHOICES,
        default='waiting',
        blank=True,
    )
    documents_status = models.CharField(
        'Документы',
        max_length=50,
        choices=DOC_STATUS_CHOICES,
        default='not_ready',
        blank=True,
    )
    comments = models.TextField('Комментарии', blank=True)

    application = models.ForeignKey(
        'Application',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='application_uuid',
        related_name='inspection_records',
        to_field='uuid',
    )
    created_by = models.ForeignKey(
        'accounts.Account',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='created_by_account_uuid',
        to_field='uuid',
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'applications_inspectionrecord'
        verbose_name = 'Запись досмотра'
        verbose_name_plural = 'Алан досмотра'
        ordering = ['inspection_date_plan', 'id']

    def __str__(self):
        return f'{self.number} — {self.client} ({self.commodity})'
