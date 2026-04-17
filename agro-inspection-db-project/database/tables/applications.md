# applications

## Назначение
Главная таблица заявок.

## Тип сущности
Основная таблица.

## Поля
| Поле | Тип | Обязательное | Источник | Описание |
|---|---|---|---|---|
| id | UUID | да | система | технический PK |
| application_number | TEXT | да | ручной ввод | бизнес-номер заявки |
| status_id | UUID | да | справочник | статус заявки |
| sender_ru_id | UUID | да | справочник | отправитель на русском |
| sender_power_of_attorney_id | UUID | нет | справочник | доверенность отправителя |
| sender_en_manual | TEXT | да | ручной ввод | отправитель на английском |
| receiver_id | UUID | да | справочник | получатель |
| product_id | UUID | да | справочник | продукт на русском |
| product_name_en_manual | TEXT | да | ручной ввод | продукт на английском |
| harvest_year | INTEGER | да | ручной ввод | год урожая |
| manufacture_date | DATE | да | ручной ввод | дата выработки |
| purpose_id | UUID | да | справочник | назначение продукции |
| weight_mt | NUMERIC | да | ручной ввод | вес партии |
| packing_type_id | UUID | да | справочник | упаковка |
| import_country_id | UUID | да | справочник | страна ввоза |
| discharge_port_ru_manual | TEXT | да | ручной ввод | порт выгрузки RU |
| discharge_port_en_manual | TEXT | да | ручной ввод | порт выгрузки EN |
| additional_declaration | TEXT | нет | ручной ввод | дополнительная декларация |
| representative_id | UUID | да | справочник | представитель |
| sampling_place_id | UUID | да | справочник | место отбора |
| laboratory_id | UUID | да | справочник | лаборатория |
| contract_number_manual | TEXT | да | ручной ввод | номер контракта |
| contract_date_manual | DATE | да | ручной ввод | дата контракта |
| planned_inspection_date | DATE | да | ручной ввод | дата начала инспекции |
| created_at | TIMESTAMP | да | система | дата создания |
| updated_at | TIMESTAMP | да | система | дата изменения |

## Уникальные ограничения
- `application_number` должен быть уникальным.

## Внешние ключи
- status_id -> dict_application_statuses.id
- sender_ru_id -> dict_senders_ru.id
- sender_power_of_attorney_id -> sender_powers_of_attorney.id
- receiver_id -> dict_receivers.id
- product_id -> dict_products.id
- purpose_id -> dict_product_purposes.id
- packing_type_id -> dict_packing_types.id
- import_country_id -> dict_countries.id
- representative_id -> dict_representatives.id
- sampling_place_id -> dict_sampling_places.id
- laboratory_id -> dict_laboratories.id
