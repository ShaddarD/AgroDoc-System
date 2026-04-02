from django.core.management.base import BaseCommand
from reference.models import (
    ApplicationStatus, PackingType, SenderRu, Country,
)


class Command(BaseCommand):
    help = 'Инициализация справочников начальными данными'

    def handle(self, *args, **options):
        # Статусы заявки
        statuses = [
            ('draft', 'Черновик', 1),
            ('in_progress', 'В работе', 2),
            ('done', 'Выполнено', 3),
        ]
        for code, name, order in statuses:
            ApplicationStatus.objects.get_or_create(code=code, defaults={'name': name, 'sort_order': order})

        # Типы упаковки
        packing_types = ['НАВАЛ', 'БИГ-БЭГ', 'МЕШКИ', 'КОНТЕЙНЕР', 'ПАЛЛЕТЫ']
        for pt in packing_types:
            PackingType.objects.get_or_create(name=pt)

        # Начальный отправитель
        SenderRu.objects.get_or_create(
            name='ООО "Блэк Си Групп-Логистик"',
            defaults={
                'legal_address': '353960, Краснодарский край, г.Новороссийск, с.Цемдолина, ул.Борисовская, д.2А, офис 1',
                'actual_address': '353900, Краснодарский край, г.Новороссийск, ул. Губернского д. 30, офис 401',
                'inn': '2315992271',
                'kpp': '231501001',
                'ogrn': '1162315056111',
            }
        )

        # Страны
        countries = [
            ('Российская Федерация', 'Russian Federation', 'RU'),
            ('Казахстан', 'Kazakhstan', 'KZ'),
            ('Китай', 'China', 'CN'),
            ('Турция', 'Turkey', 'TR'),
            ('Египет', 'Egypt', 'EG'),
        ]
        for name_ru, name_en, iso in countries:
            Country.objects.get_or_create(
                name_ru=name_ru,
                defaults={'name_en': name_en, 'iso_code': iso}
            )

        self.stdout.write(self.style.SUCCESS('Справочники успешно инициализированы'))
