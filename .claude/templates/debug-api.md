# Debug API / Network Issue

## Контекст

* Endpoint:
* Где вызывается: (frontend файл)
* Метод: (GET/POST/etc)

## Симптом

Что не работает:
(например: 500, 403, undefined, пустой ответ)

## Network

* URL:
* Method:
* Status:
* Request payload:
* Response body:

## Frontend код

(axios / fetch вызов)

## Backend код

(view / serializer)

## Ошибки

* console:
* backend logs:

---

## Задача для Claude

1. Определи, где проблема:

   * frontend
   * API слой
   * backend
   * DB

2. Найди наиболее вероятную причину

3. Проверь:

   * payload mismatch
   * response mismatch
   * endpoint существует ли
   * permissions
   * serializer validation

4. Дай минимальный фикс

5. Покажи исправленный код

6. Скажи, что проверить после
