# reference/models.py

from django.db import models

class Applicant(models.Model):
    """Справочник заявителей (юридические лица)"""
    
    name_rus = models.CharField('Наименование (рус)', max_length=500)
    name_eng = models.CharField('Наименование (eng)', max_length=500, blank=True)
    legal_address = models.TextField('Юридический адрес')
    actual_address = models.TextField('Фактический адрес', blank=True)
    inn = models.CharField('ИНН', max_length=20)
    kpp = models.CharField('КПП', max_length=20, blank=True)
    ogrn = models.CharField('ОГРН', max_length=30, blank=True)
    contact_person = models.CharField('Контактное лицо', max_length=200, blank=True)
    phone = models.CharField('Телефон', max_length=50, blank=True)
    email = models.EmailField('Email', blank=True)
    is_active = models.BooleanField('Активен', default=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Заявитель'
        verbose_name_plural = 'Заявители'
    
    def __str__(self):
        return self.name_rus


class Product(models.Model):
    """Справочник продукции"""
    
    name_rus = models.CharField('Наименование (рус)', max_length=500)
    name_eng = models.CharField('Наименование (eng)', max_length=500)
    botanical_name = models.CharField('Ботаническое название', max_length=500)
    tnved_code = models.CharField('Код ТН ВЭД', max_length=20)
    is_active = models.BooleanField('Активен', default=True)
    
    class Meta:
        verbose_name = 'Продукция'
        verbose_name_plural = 'Продукция'
    
    def __str__(self):
        return f"{self.name_rus} ({self.tnved_code})"


class Importer(models.Model):
    """Справочник импортеров (получателей)"""
    
    name_eng = models.CharField('Наименование (eng)', max_length=500)
    address_eng = models.TextField('Адрес (eng)')
    country = models.CharField('Страна', max_length=100)
    city = models.CharField('Город', max_length=200)
    is_active = models.BooleanField('Активен', default=True)
    
    class Meta:
        verbose_name = 'Импортер'
        verbose_name_plural = 'Импортеры'
    
    def __str__(self):
        return f"{self.name_eng} ({self.country})"


class InspectionPlace(models.Model):
    """Справочник мест инспекции/отбора проб"""
    
    name = models.CharField('Название', max_length=500)
    address = models.TextField('Адрес')
    is_active = models.BooleanField('Активен', default=True)
    
    class Meta:
        verbose_name = 'Место инспекции'
        verbose_name_plural = 'Места инспекции'
    
    def __str__(self):
        return self.name


class PackingType(models.Model):
    """Справочник типов упаковки"""
    
    name = models.CharField('Название', max_length=100)
    name_eng = models.CharField('Название (eng)', max_length=100, blank=True)
    
    class Meta:
        verbose_name = 'Тип упаковки'
        verbose_name_plural = 'Типы упаковки'
    
    def __str__(self):
        return self.name