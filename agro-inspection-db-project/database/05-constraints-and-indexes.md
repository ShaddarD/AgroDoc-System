# Constraints and Indexes

## Обязательные ограничения
- unique(application_number)
- unique(application_id, container_number)
- внешние ключи на все справочники
- not null на обязательные поля

## Рекомендуемые индексы
- applications(application_number)
- applications(status_id)
- applications(sender_ru_id)
- applications(receiver_id)
- applications(product_id)
- applications(planned_inspection_date)
