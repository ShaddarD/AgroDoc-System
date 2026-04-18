from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = 'Инициализация начальных данных (справочники)'

    def handle(self, *args, **options):
        roles = [
            ('admin',   'Администратор', 'Administrator'),
            ('manager', 'Менеджер',      'Manager'),
            ('user',    'Пользователь',  'User'),
        ]
        with connection.cursor() as cur:
            for code, name_ru, name_en in roles:
                cur.execute(
                    """
                    INSERT INTO lookup_role_codes (role_code, display_name_ru, display_name_en)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (role_code) DO UPDATE
                        SET display_name_ru = EXCLUDED.display_name_ru,
                            display_name_en = EXCLUDED.display_name_en
                    """,
                    [code, name_ru, name_en],
                )
        self.stdout.write(self.style.SUCCESS('Инициализация завершена'))
