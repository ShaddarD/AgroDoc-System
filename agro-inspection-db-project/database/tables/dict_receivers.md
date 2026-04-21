# dict_receivers

## Назначение
Справочник получателей.

## Поля
| Поле | Тип | Обязательное | Описание |
|---|---|---|---|
| id | UUID | да | PK |
| name_en | TEXT | да | наименование |
| legal_address | TEXT | да | юридический адрес |
| actual_address | TEXT | да | фактический адрес |
| inn | TEXT | нет | ИНН |
| kpp | TEXT | нет | КПП |
| ogrn | TEXT | нет | ОГРН/ОГРНИП |
| is_active | BOOLEAN | да | активность |
