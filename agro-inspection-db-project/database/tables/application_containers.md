# application_containers

## Назначение
Контейнеры заявки.

## Тип сущности
Дочерняя таблица.

## Поля
| Поле | Тип | Обязательное | Источник | Описание |
|---|---|---|---|---|
| id | UUID | да | система | PK |
| application_id | UUID | да | FK | ссылка на заявку |
| container_number | TEXT | да | ручной ввод | номер контейнера |
| sort_order | INTEGER | нет | система | порядок вывода |

## Ограничения
- unique(application_id, container_number)
