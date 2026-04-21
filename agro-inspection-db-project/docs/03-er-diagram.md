# ER Diagram

## Текстовая схема

```text
dict_application_statuses
    └──< applications >── dict_senders_ru
            │                 │
            │                 └──< sender_powers_of_attorney
            │
            ├───────────────> dict_receivers
            ├───────────────> dict_products
            │                    ├──────────> dict_gosts
            │                    ├──────────> dict_tr_ts
            │                    └──────────> dict_tr_ts_sampling
            │
            ├───────────────> dict_product_purposes
            ├───────────────> dict_packing_types
            ├───────────────> dict_countries
            ├───────────────> dict_representatives
            ├───────────────> dict_sampling_places
            ├───────────────> dict_laboratories
            │
            ├──< application_containers
            ├──< application_certificates >── dict_certificates
            └──< application_regulations >── dict_regulations
```

## Mermaid
См. файл `../diagrams/er-diagram.mmd`.
