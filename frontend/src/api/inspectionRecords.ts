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

    number = models.CharField(max_length=100, blank=True)
    client = models.CharField(max_length=300, blank=True)
    manager = models.CharField(max_length=200, blank=True)
    commodity = models.CharField(max_length=200, blank=True)
    container_count = models.TextField(blank=True)
    container_type = models.CharField(
        max_length=5,
        blank=True,
        choices=[('x20', 'x20'), ('x40', 'x40')],
    )
    weight = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    pod = models.CharField(max_length=200, blank=True)
    terminal = models.CharField(max_length=200, blank=True)
    quarantine = models.CharField(max_length=50, choices=QUARANTINE_CHOICES, blank=True)
    inspection_date_plan = models.DateField(null=True, blank=True)
    fss_date_plan = models.DateField(null=True, blank=True)
    cargo_status = models.CharField(max_length=50, choices=CARGO_STATUS_CHOICES, default='waiting', blank=True)
    documents_status = models.CharField(max_length=50, choices=DOC_STATUS_CHOICES, default='not_ready', blank=True)
    comments = models.TextField(blank=True)

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
        ordering = ['inspection_date_plan', 'id']

    def __str__(self):
        return f'{self.number} — {self.client} ({self.commodity})'