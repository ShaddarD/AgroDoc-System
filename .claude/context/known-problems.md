---

## Claude Workflow Extensions

Ниже описаны дополнительные команды, шаблоны и правила работы Claude в этом репозитории.

### Подключённые skill-файлы

Claude должен использовать дополнительные инструкции из файлов:

- `.claude/skills/refactor.md`
- `.claude/skills/debug.md`
- `.claude/skills/testing.md`

Когда задача связана с улучшением существующего кода — использовать `refactor.md`.
Когда задача связана с поиском причины ошибки — использовать `debug.md`.
Когда задача связана с тестированием и покрытием — использовать `testing.md`.

### Подключённые шаблоны

При постановке задач использовать шаблоны из:

- `.claude/templates/bug-report.md`
- `.claude/templates/refactor-task.md`
- `.claude/templates/test-case.md`
- `.claude/templates/api-task.md`
- `.claude/templates/frontend-task.md`
- `.claude/templates/debug-api.md`
- `.claude/templates/find-n-plus-one.md`
- `.claude/templates/split-services-selectors.md`

Если пользователь просит найти баг — сначала ориентироваться на `bug-report.md` или `debug-api.md`.
Если пользователь просит улучшить код — использовать `refactor-task.md`.
Если пользователь просит тесты — использовать `test-case.md`.
Если пользователь просит новый endpoint — использовать `api-task.md`.
Если пользователь просит UI или React-компонент — использовать `frontend-task.md`.

---

## Claude Commands

Ниже псевдо-команды. Их не нужно воспринимать как CLI-команды; это режимы работы Claude внутри репозитория.

### `/fix-bug`

Использовать, когда:
- есть traceback
- есть network error
- есть 4xx/5xx
- UI "частично работает", но ломается на действии
- есть рассинхрон frontend/backend

Алгоритм:
1. Коротко описать симптом
2. Определить слой проблемы:
   - frontend
   - API layer
   - backend view/serializer/service
   - database
   - docker/nginx/env
3. Дать 1 наиболее вероятную причину
4. Дать 2–4 альтернативные гипотезы
5. Предложить минимальный фикс
6. Показать код исправления
7. Дать regression-checklist

Важно:
- не переписывать модуль целиком
- не выдавать гипотезу за доказанный факт
- приоритетно проверять существование endpoint, payload/response mismatch, permissions, auth headers, serializer validation

### `/review-api`

Использовать, когда нужно проверить или спроектировать backend endpoint.

Алгоритм:
1. Проверить URL, HTTP method, serializer, permissions, response contract
2. Проверить валидацию и коды ответов
3. Проверить возможные N+1 и избыточные запросы
4. Проверить, не ломает ли endpoint текущий frontend
5. Показать рекомендуемый вариант кода
6. Показать request/response examples
7. Указать edge cases

Важно:
- использовать Django 4.2 + DRF idiomatic way
- не предлагать смену стека
- при изменении API явно указывать влияние на frontend

### `/review-frontend`

Использовать для React/TypeScript/AntD кода.

Алгоритм:
1. Проверить типизацию
2. Проверить loading/error/empty states
3. Проверить форму, таблицу, фильтры, async state
4. Проверить связку с API
5. Проверить лишние re-render и смешение UI/API/state
6. Дать минимальный безопасный рефакторинг

Важно:
- использовать React 18 + TypeScript + Ant Design v5
- не вносить лишние архитектурные изменения
- сохранять текущий UX, если не просят иное

### `/write-tests`

Использовать, когда нужно покрыть код тестами.

Алгоритм:
1. Сначала определить тип теста:
   - smoke
   - integration
   - regression
   - unit
2. Отдать приоритет тестам, которые ловят реальные регрессии
3. Покрыть happy path, invalid data, no permissions, not found, edge cases
4. Если чинится баг — обязательно добавить regression test
5. Показать, что ещё проверить вручную

### `/find-n-plus-one`

Использовать для Django ORM и DRF list/detail endpoint'ов.

Алгоритм:
1. Определить queryset и связанные модели
2. Проверить обращения к FK/M2M/reverse relations в serializer/property/method fields
3. Проверить, где не хватает `select_related` / `prefetch_related`
4. Проверить лишние `.count()`, `.exists()`, циклы по queryset
5. Предложить оптимизированный queryset
6. Указать, как проверить улучшение

Важно:
- не оптимизировать вслепую
- сначала показать источник N+1
- не усложнять код ради микровыигрыша без пользы

### `/split-services`

Использовать, когда код перегружен логикой и её нужно аккуратно разнести по слоям.

Алгоритм:
1. Определить текущую ответственность кода
2. Отделить:
   - selectors — чтение и выборки
   - services — бизнес-операции/изменения состояния
   - serializers — только валидация и преобразование данных
   - views — orchestration / HTTP layer
3. Сохранить поведение и API
4. Показать минимальную миграцию кода, без "переписать всё"

Важно:
- не выносить код в services/selectors ради моды
- делать это только там, где код реально стал слишком тяжёлым
- избегать избыточных абстракций

---

## Pytest Setup Policy

Для backend тестов использовать `pytest` + `pytest-django`.

### Рекомендуемые зависимости для dev/test

```txt
pytest
pytest-django
pytest-cov
factory-boy