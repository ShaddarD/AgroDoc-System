# Find N+1 Task

## Контекст
- Django app:
- Endpoint / view:
- Serializer:
- Queryset:

## Симптом
- медленный список / детали
- много SQL запросов
- nested data тормозит

## Код
(вставь view / queryset / serializer)

## Задача для Claude
1. Найди возможный N+1
2. Объясни, где он появляется
3. Предложи оптимизацию через select_related/prefetch_related/annotate
4. Покажи обновлённый код
5. Скажи, как проверить улучшение