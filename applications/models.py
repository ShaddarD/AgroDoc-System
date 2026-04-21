import uuid
from django.db import models
from django.contrib.auth.models import User


class Application(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    application_number = models.CharField(max_length=100, null=True, blank=True, unique=True)
    applicant_counterparty = models.ForeignKey(
        'accounts.Counterparty', on_delete=models.RESTRICT, null=True, blank=True,
        db_column='applicant_counterparty_uuid', related_name='applications_as_applicant',
    )
    applicant_account = models.ForeignKey(
        'accounts.Account', on_delete=models.RESTRICT, null=True, blank=True,
        db_column='applicant_account_uuid', related_name='applications_as_applicant',
    )
    terminal = models.ForeignKey(
        'reference.Terminal', on_delete=models.RESTRICT, null=True, blank=True,
        db_column='terminal_uuid',
    )
    product = models.ForeignKey(
        'reference.Product', on_delete=models.RESTRICT, null=True, blank=True,
        db_column='product_uuid',
    )
    power_of_attorney = models.ForeignKey(
        'reference.PowerOfAttorney', on_delete=models.SET_NULL, null=True, blank=True,
        db_column='power_of_attorney_uuid',
    )
    status_code = models.CharField(max_length=50, default='draft')
    submitted_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
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
    """Алан досмотра — оперативный трекинг отгрузок."""

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

    number = models.CharField('№', max_length=100, blank=True)
    client = models.CharField('Клиент', max_length=300, blank=True)
    manager = models.CharField('Менеджер', max_length=200, blank=True)
    commodity = models.CharField('Культура', max_length=200, blank=True)
    container_count = models.TextField('Номера контейнеров', blank=True)
    container_type = models.CharField('Тип контейнера', max_length=5, blank=True,
                                      choices=[('x20', 'x20'), ('x40', 'x40')])
    weight = models.DecimalField('Вес (кг)', max_digits=12, decimal_places=2, null=True, blank=True)
    pod = models.CharField('POD', max_length=200, blank=True)
    terminal = models.CharField('Терминал', max_length=200, blank=True)
    quarantine = models.CharField('Карантинки', max_length=50, choices=QUARANTINE_CHOICES, blank=True)
    inspection_date_plan = models.DateField('ДОСМОТР (ПЛАН)', null=True, blank=True)
    fss_date_plan = models.DateField('Дата выдачи ФСС (ПЛАН)', null=True, blank=True)
    cargo_status = models.CharField('Груз', max_length=50, choices=CARGO_STATUS_CHOICES,
                                    default='waiting', blank=True)
    documents_status = models.CharField('Документы', max_length=50, choices=DOC_STATUS_CHOICES,
                                        default='not_ready', blank=True)
    comments = models.TextField('Комментарии', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = 'Запись досмотра'
        verbose_name_plural = 'Алан досмотра'
        ordering = ['inspection_date_plan', 'id']

    def __str__(self):
        return f'{self.number} — {self.client} ({self.commodity})'
