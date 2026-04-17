import uuid
from django.db import models
from django.contrib.auth.models import User

from reference.models import (
    ApplicationStatus, SenderRu, SenderPowerOfAttorney, Receiver,
    Product, ProductPurpose, PackingType, Country, Representative,
    SamplingPlace, Laboratory, Certificate, Regulation,
)


class Application(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    application_number = models.TextField(unique=True)
    status = models.ForeignKey(
        ApplicationStatus, on_delete=models.PROTECT, null=True, blank=True,
        verbose_name='Статус'
    )
    sender_ru = models.ForeignKey(
        SenderRu, on_delete=models.PROTECT, null=True, blank=True,
        verbose_name='Отправитель (рус)'
    )
    sender_power_of_attorney = models.ForeignKey(
        SenderPowerOfAttorney, on_delete=models.SET_NULL, null=True, blank=True,
        verbose_name='Доверенность'
    )
    sender_en_manual = models.TextField('Отправитель (eng)', blank=True)
    receiver = models.ForeignKey(
        Receiver, on_delete=models.PROTECT, null=True, blank=True,
        verbose_name='Получатель'
    )
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, null=True, blank=True,
        verbose_name='Продукция'
    )
    product_name_en_manual = models.TextField('Продукт (eng)', blank=True)
    harvest_year = models.IntegerField('Год урожая', null=True, blank=True)
    manufacture_date = models.DateField('Дата выработки', null=True, blank=True)
    purpose = models.ForeignKey(
        ProductPurpose, on_delete=models.PROTECT, null=True, blank=True,
        verbose_name='Назначение'
    )
    weight_mt = models.DecimalField('Вес (MT)', max_digits=12, decimal_places=3, null=True, blank=True)
    packing_type = models.ForeignKey(
        PackingType, on_delete=models.PROTECT, null=True, blank=True,
        verbose_name='Тип упаковки'
    )
    import_country = models.ForeignKey(
        Country, on_delete=models.PROTECT, null=True, blank=True,
        verbose_name='Страна ввоза'
    )
    discharge_port_ru_manual = models.TextField('Порт выгрузки (рус)', blank=True)
    discharge_port_en_manual = models.TextField('Порт выгрузки (eng)', blank=True)
    additional_declaration = models.TextField('Дополнительная декларация', blank=True)
    representative = models.ForeignKey(
        Representative, on_delete=models.PROTECT, null=True, blank=True,
        verbose_name='Представитель'
    )
    sampling_place = models.ForeignKey(
        SamplingPlace, on_delete=models.PROTECT, null=True, blank=True,
        verbose_name='Место отбора'
    )
    laboratory = models.ForeignKey(
        Laboratory, on_delete=models.PROTECT, null=True, blank=True,
        verbose_name='Лаборатория'
    )
    contract_number_manual = models.TextField('Номер контракта', blank=True)
    contract_date_manual = models.DateField('Дата контракта', null=True, blank=True)
    planned_inspection_date = models.DateField('Дата инспекции (план)', null=True, blank=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True,
        verbose_name='Создал'
    )

    class Meta:
        db_table = 'applications'
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
        ordering = ['-created_at']

    def __str__(self):
        return f"Заявка №{self.application_number}"

    def save(self, *args, **kwargs):
        if not self.application_number:
            super().save(*args, **kwargs)
            self.application_number = f"APP-{self.created_at.strftime('%Y%m')}-{str(self.id)[:8].upper()}"
            kwargs['force_insert'] = False
        super().save(*args, **kwargs)


class ApplicationContainer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    application = models.ForeignKey(
        Application, on_delete=models.CASCADE, related_name='containers',
        verbose_name='Заявка'
    )
    container_number = models.TextField('Номер контейнера')
    sort_order = models.IntegerField('Порядок', null=True, blank=True)

    class Meta:
        db_table = 'application_containers'
        verbose_name = 'Контейнер'
        verbose_name_plural = 'Контейнеры'
        unique_together = [('application', 'container_number')]

    def __str__(self):
        return self.container_number


class ApplicationCertificate(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    application = models.ForeignKey(
        Application, on_delete=models.CASCADE, related_name='certificates',
        verbose_name='Заявка'
    )
    certificate = models.ForeignKey(
        Certificate, on_delete=models.PROTECT, verbose_name='Сертификат'
    )
    copies_count = models.IntegerField('Кол-во копий', null=True, blank=True)
    is_required = models.BooleanField('Обязательный', null=True, blank=True)

    class Meta:
        db_table = 'application_certificates'
        verbose_name = 'Сертификат заявки'
        verbose_name_plural = 'Сертификаты заявки'

    def __str__(self):
        return str(self.certificate)


class ApplicationRegulation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    application = models.ForeignKey(
        Application, on_delete=models.CASCADE, related_name='regulations',
        verbose_name='Заявка'
    )
    regulation = models.ForeignKey(
        Regulation, on_delete=models.PROTECT, verbose_name='Регламент'
    )
    comment = models.TextField('Комментарий', blank=True)

    class Meta:
        db_table = 'application_regulations'
        verbose_name = 'Регламент заявки'
        verbose_name_plural = 'Регламенты заявки'

    def __str__(self):
        return str(self.regulation)


class GeneratedFile(models.Model):
    FILE_TYPE_CHOICES = [
        ('cokz', 'Заявка ЦОКЗ'),
        ('fito1', 'Фитосертификат лист 1'),
        ('fito2', 'Фитосертификат лист 2'),
        ('act', 'Акт досмотра'),
        ('other', 'Другое'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    application = models.ForeignKey(
        Application, on_delete=models.CASCADE, related_name='files',
        verbose_name='Заявка'
    )
    file_name = models.CharField('Имя файла', max_length=255)
    file_path = models.FileField('Файл', upload_to='generated_docs/%Y/%m/%d/')
    file_type = models.CharField('Тип файла', max_length=20, choices=FILE_TYPE_CHOICES)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='Создал')

    class Meta:
        verbose_name = 'Сгенерированный файл'
        verbose_name_plural = 'Сгенерированные файлы'

    def __str__(self):
        return self.file_name


class InspectionRecord(models.Model):
    """Алан досмотра — оперативный трекинг отгрузок"""

    QUARANTINE_CHOICES = [
        ('own', 'Свои'),
        ('client', 'Клиентские'),
        ('shared', 'Совместные'),
        ('other', 'Другое'),
    ]

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

    number = models.CharField('№', max_length=100, blank=True)
    client = models.CharField('Клиент', max_length=300, blank=True)
    manager = models.CharField('Менеджер', max_length=200, blank=True)
    commodity = models.CharField('Культура', max_length=200, blank=True)
    container_count = models.TextField('Номера контейнеров', blank=True,
                                       help_text='Через запятую, напр.: ABCD1234567, EFGH2345678')
    container_type = models.CharField('Тип контейнера', max_length=5, blank=True,
                                      choices=[('x20', 'x20'), ('x40', 'x40')])
    weight = models.DecimalField('Вес (кг)', max_digits=12, decimal_places=2, null=True, blank=True)
    pod = models.CharField('POD', max_length=200, blank=True, help_text='Порт назначения, напр.: Циндао, Китай')
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
        return f"{self.number} — {self.client} ({self.commodity})"


class ShipmentBatch(models.Model):
    """Реестр затарки — партия контейнеров"""

    STATUS_CHOICES = [
        ('draft', 'Черновик'),
        ('ready', 'Готов к привязке'),
        ('linked', 'Привязан к заявке'),
        ('closed', 'Закрыт'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    batch_number = models.CharField('Номер реестра', max_length=100, blank=True)
    batch_date = models.DateField('Дата реестра', null=True, blank=True)
    destination = models.CharField('Направление/Станция', max_length=200, blank=True)
    sender_ru = models.ForeignKey(
        'reference.SenderRu', on_delete=models.PROTECT, null=True, blank=True,
        verbose_name='Отправитель'
    )
    application = models.ForeignKey(
        'Application', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='shipment_batches', verbose_name='Заявка'
    )
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='draft')
    notes = models.TextField('Примечания', blank=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, verbose_name='Создал'
    )

    class Meta:
        db_table = 'shipment_batches'
        verbose_name = 'Реестр затарки'
        verbose_name_plural = 'Реестры затарки'
        ordering = ['-created_at']

    def __str__(self):
        return f"Реестр {self.batch_number or self.id} от {self.batch_date or '—'}"


class ContainerShipment(models.Model):
    """Запись о контейнере в реестре затарки"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    batch = models.ForeignKey(
        ShipmentBatch, on_delete=models.CASCADE, related_name='containers',
        verbose_name='Реестр'
    )
    sort_order = models.IntegerField('№ п/п', null=True, blank=True)

    # Контейнер
    container_number = models.CharField('Номер контейнера', max_length=20)
    container_type = models.CharField('Тип контейнера', max_length=10, blank=True)  # 40HC, 20DV

    # Весовые данные при затарке
    tare_weight = models.IntegerField('Тара контейнера (кг)', null=True, blank=True)
    gross_weight = models.IntegerField('Вес брутто при затарке (кг)', null=True, blank=True)
    net_weight = models.IntegerField('Вес нетто при затарке (кг)', null=True, blank=True)
    max_load = models.IntegerField('Макс. нагрузка (кг)', null=True, blank=True)

    # Пломба и вагон
    seal_number = models.CharField('Номер пломбы', max_length=50, blank=True)
    wagon_number = models.CharField('Номер вагона', max_length=50, blank=True)

    # Количество и погрузка
    bags_count = models.IntegerField('Количество мест', null=True, blank=True)
    loading_date = models.DateField('Дата погрузки', null=True, blank=True)

    # Накладная
    waybill_number = models.CharField('Номер накладной', max_length=50, blank=True)
    waybill_date = models.DateField('Дата накладной', null=True, blank=True)

    # Железнодорожные весовые данные
    railway_gross = models.IntegerField('Ж/д брутто (кг)', null=True, blank=True)
    railway_tare = models.IntegerField('Ж/д тара (кг)', null=True, blank=True)
    railway_net = models.IntegerField('Ж/д нетто (кг)', null=True, blank=True)
    railway_date = models.DateField('Дата ж/д взвешивания', null=True, blank=True)

    # Дополнительно
    notes = models.TextField('Примечания', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'container_shipments'
        verbose_name = 'Контейнер в реестре'
        verbose_name_plural = 'Контейнеры в реестре'
        ordering = ['sort_order', 'created_at']

    def __str__(self):
        return f"{self.container_number} ({self.batch})"


class ApplicationHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    application = models.ForeignKey(
        Application, on_delete=models.CASCADE, related_name='history',
        verbose_name='Заявка'
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='Пользователь')
    action = models.CharField('Действие', max_length=200)
    changes = models.JSONField('Изменения', default=dict, blank=True)
    created_at = models.DateTimeField('Дата', auto_now_add=True)

    class Meta:
        verbose_name = 'История'
        verbose_name_plural = 'История изменений'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.created_at.strftime('%d.%m.%Y %H:%M')} - {self.action}"
