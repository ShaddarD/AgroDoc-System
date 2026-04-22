# /find-n-plus-one

Задача: найти и устранить N+1 в Django ORM/DRF.

Порядок:
1. Найти queryset
2. Найти связанные модели, к которым обращаются в serializer/view/template
3. Найти доступы к relation в циклах
4. Проверить SerializerMethodField, nested serializer, property
5. Предложить select_related/prefetch_related/annotate
6. Показать обновлённый queryset
7. Предложить способ проверки улучшения

Формат ответа:
- Где N+1
- Почему он возникает
- Исправление
- Обновлённый код
- Как проверить