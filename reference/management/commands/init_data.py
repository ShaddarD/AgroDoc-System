# reference/management/commands/init_data.py

from django.core.management.base import BaseCommand
from reference.models import PackingType, Applicant

class Command(BaseCommand):
    help = 'Инициализация справочников начальными данными'
    
    def handle(self, *args, **options):
        # Типы упаковки
        packing_types = ['НАВАЛ', 'БИГ-БЭГ', 'МЕШКИ', 'КОНТЕЙНЕР', 'ПАЛЛЕТЫ']
        for pt in packing_types:
            PackingType.objects.get_or_create(name=pt)
        
        # Начальный заявитель из ваших данных
        Applicant.objects.get_or_create(
            name_rus='ООО "Блэк Си Групп-Логистик"',
            name_eng='Black Sea Group Logistic LLC',
            legal_address='353960, Краснодарский край, г.Новороссийск, с.Цемдолина, ул.Борисовская, д.2А, офис 1',
            actual_address='353900, Краснодарский край, г.Новороссийск, ул. Губернского д. 30, офис 401',
            inn='2315992271',
            kpp='231501001',
            ogrn='1162315056111',
            contact_person='Козюпа С.В.',
            phone='+79180611074',
            email='kozyupa@bsglogistics.ru'
        )
        
        self.stdout.write(self.style.SUCCESS('Справочники успешно инициализированы'))