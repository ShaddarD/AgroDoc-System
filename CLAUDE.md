# AgroDoc-System — Claude Context

## Project Overview

Fullstack система для работы с заявками, актами и документами.

### Стек

* Backend: Django 4.2 + Django REST Framework
* Frontend: React 18 + TypeScript + Ant Design v5
* Database: PostgreSQL 15
* Infra: Docker Compose + Nginx

---

## Project Structure

### Backend Apps

* `accounts/` — пользователи, роли, авторизация
* `applications/` — заявки, бизнес-логика, документы
* `reference/` — справочники

Ключевые места:

* `applications/services.py`
* `applications/document_generator.py`
* `accounts/models.py`
* `applications/models.py`

### Frontend

* `frontend/src/api/` — API слой
* `frontend/src/store/` — state
* `frontend/src/components/`
* `frontend/src/pages/`

---

## Known Critical Issue

⚠️ Важно:

Frontend уже вызывает:

* `generateDocuments`
* `downloadFile`

Но backend endpoints для этого могут отсутствовать.

👉 Всегда проверяй:

* существует ли endpoint
* совпадает ли payload/response

---

# Claude Workflow

## Skills

Используй:

* `.claude/skills/refactor.md`
* `.claude/skills/debug.md`
* `.claude/skills/testing.md`

---

## Templates

Используй:

* bug-report.md
* debug-api.md
* refactor-task.md
* test-case.md
* api-task.md
* frontend-task.md
* find-n-plus-one.md
* split-services-selectors.md

---

# Claude Commands

## /fix-bug

Использовать при ошибках.

Алгоритм:

1. Симптом
2. Слой проблемы
3. Причина
4. Проверка
5. Минимальный фикс
6. Regression test

Приоритет проверки:

* endpoint существует ли
* payload/response mismatch
* permissions/auth
* serializer validation
* service logic
* DB

---

## /review-api

Проверить:

* route
* method
* serializer
* permissions
* validation
* status codes
* queryset

---

## /review-frontend

Проверить:

* типизацию
* loading/error states
* формы
* API интеграцию
* re-render

---

## /write-tests

Приоритет:

1. smoke
2. integration
3. regression
4. unit

---

## /find-n-plus-one

Проверять:

* serializer fields
* relations
* циклы
* queryset

Использовать:

* select_related
* prefetch_related
* annotate

---

## /split-services

Разделять:

* selectors → чтение
* services → бизнес-логика
* serializers → валидация
* views → HTTP

---

# Testing Policy

Использовать:

* pytest
* pytest-django
* factory-boy

## Структура тестов

```text
tests/
├─ conftest.py
├─ api/
├─ integration/
├─ regression/
└─ smoke/
```

## Приоритет тестов

1. auth
2. permissions
3. applications CRUD
4. documents
5. file download/upload
6. regression bugs

---

# ORM Performance

Проверять:

* N+1
* nested serializers
* queryset loops

---

# Refactoring Rules

* не переписывать всё
* минимальные изменения
* сохранять API
* не менять стек

---

# Debug Rules

* сначала локализовать проблему
* не гадать
* давать гипотезы с приоритетом
* давать минимальный фикс

---

# Frontend Rules

* строгая типизация
* Ant Design v5
* loading/error/empty states
* не ломать UX

---

# Backend Rules

* DRF best practices
* validation + permissions
* error handling
* производительность ORM

---

# Project Priorities

Всегда проверяй:

* auth (JWT)
* permissions
* applications
* documents
* file generation/download
* frontend ↔ backend контракт
* nginx/media/static
* docker/env

Если есть сомнения:
→ выбирай минимально рискованное решение
→ явно указывай допущения
