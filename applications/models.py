# applications/models.py

from django.db import models
from django.contrib.auth.models import User
from reference.models import Applicant, Product, Importer, InspectionPlace
import json

class Application(models.Model):
    """Основная модель заявки"""
    
    STATUS_CHOICES = [
        ('draft', 'Черновик'),
        ('completed', 'Сформирован'),
        ('archived', 'В архиве'),
    ]
    
    # Основная информация
    application_number = models.CharField('Номер заявки', max_length=50, blank=True, unique=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='Создал')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='draft')
    
    # Блок 1: Заявитель (из справочника или свободный ввод)
    applicant = models.ForeignKey(Applicant, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Заявитель')
    applicant_custom = models.TextField('Заявитель (свободный ввод)', blank=True)
    poruchenie = models.TextField('По поручению', blank=True)
    doverennost = models.CharField('Доверенность', max_length=200, blank=True)
    
    # Блок 2: Отправитель (Экспортер)
    exporter_rus = models.CharField('Экспортер (рус)', max_length=500)
    exporter_eng = models.CharField('Экспортер (eng)', max_length=500)
    exporter_address = models.TextField('Адрес экспортера')
    exporter_inn = models.CharField('ИНН экспортера', max_length=20, blank=True)
    exporter_kpp = models.CharField('КПП экспортера', max_length=20, blank=True)
    exporter_ogrn = models.CharField('ОГРН экспортера', max_length=30, blank=True)
    
    # Блок 3: Получатель (Импортер)
    importer = models.ForeignKey(Importer, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Импортер')
    importer_custom = models.TextField('Импортер (свободный ввод)', blank=True)
    importer_name_eng = models.CharField('Импортер (eng)', max_length=500, blank=True)
    importer_address_eng = models.TextField('Адрес импортера (eng)', blank=True)
    importer_country = models.CharField('Страна импортера', max_length=100, blank=True)
    importer_city = models.CharField('Город назначения', max_length=200, blank=True)
    
    # Блок 4: Продукция и отгрузка
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Продукция')
    product_custom = models.TextField('Продукция (свободный ввод)', blank=True)
    product_rus = models.CharField('Продукция (рус)', max_length=500, blank=True)
    product_eng = models.CharField('Продукция (eng)', max_length=500, blank=True)
    botanical_name = models.CharField('Ботаническое название', max_length=500, blank=True)
    tnved_code = models.CharField('Код ТН ВЭД', max_length=20, blank=True)
    
    weight_tons = models.DecimalField('Вес (тонн)', max_digits=10, decimal_places=3)
    weight_mt = models.DecimalField('Вес (MT)', max_digits=10, decimal_places=2)
    
    packing_type = models.CharField('Тип упаковки', max_length=100)
    places_count = models.CharField('Количество мест', max_length=200)
    containers_list = models.TextField('Номера контейнеров', blank=True)
    
    inspection_place = models.ForeignKey(InspectionPlace, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Место инспекции')
    inspection_place_custom = models.TextField('Место инспекции (свободный ввод)', blank=True)
    
    origin_country = models.CharField('Страна происхождения', max_length=200, default='Российская Федерация')
    
    # Блок 5: Документы (храним в JSON)
    documents_needed = models.JSONField('Необходимые документы', default=dict, blank=True)
    
    # Блок 6: Дополнительная информация
    argus_registrations = models.TextField('Регистрации в Аргус', blank=True, 
                                          help_text='Номера регистраций через запятую')
    inspection_date = models.DateField('Предполагаемая дата инспекции', null=True, blank=True)
    permit_number = models.CharField('Номер разрешения (Permit)', max_length=200, blank=True)
    notes = models.TextField('Примечания', blank=True)
    
    # Контактная информация заявителя
    contact_phone = models.CharField('Контактный телефон', max_length=50, blank=True)
    contact_email = models.EmailField('Контактный email', blank=True)
    
    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Заявка №{self.application_number or 'б/н'} от {self.created_at.strftime('%d.%m.%Y')}"
    
    def save(self, *args, **kwargs):
        # Генерируем номер заявки, если его нет
        if not self.application_number:
            from django.utils import timezone
            now = self.created_at if self.created_at else timezone.now()
            last_id = Application.objects.count() + 1
            self.application_number = f"APP-{now.strftime('%Y%m')}-{last_id:04d}"
        super().save(*args, **kwargs)


class GeneratedFile(models.Model):
    """Модель для хранения сгенерированных файлов"""
    
    FILE_TYPE_CHOICES = [
        ('cokz', 'Заявка ЦОКЗ'),
        ('fito1', 'Фитосертификат лист 1'),
        ('fito2', 'Фитосертификат лист 2'),
        ('act', 'Акт досмотра'),
        ('other', 'Другое'),
    ]
    
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='files', verbose_name='Заявка')
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


class ApplicationHistory(models.Model):
    """История изменений заявки"""
    
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='history', verbose_name='Заявка')
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