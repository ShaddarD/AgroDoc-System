# Status Transitions

## Допустимые переходы
- `draft -> in_progress`
- `in_progress -> done`

## Рекомендация
Логику переходов статусов обрабатывать отдельным endpoint, а не обычным PATCH всей заявки.
