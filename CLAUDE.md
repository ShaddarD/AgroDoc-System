# AgroDoc-System — Master Project File

## Назначение системы
Система автоматизации оформления заявок на инспекцию/досмотр/сертификацию сельскохозяйственной продукции.  
**Стек:** Django 4.2 (DRF) + React 18 (TypeScript, Ant Design v5) + PostgreSQL 15 + Docker Compose.

---

## Структура монорепо

```
AgroDoc-System/
├── agro_doc/          # Django project root (settings, urls)
├── accounts/          # Пользователи, контрагенты, JWT-аутентификация
├── applications/      # Заявки + план досмотра (InspectionRecord)
├── reference/         # Справочники (4 модели)
├── frontend/          # React SPA
├── templates/         # Django-шаблоны (admin)
├── media/             # Загрузки
├── agro-inspection-db-project/  # Проектная документация (API + DB specs)
├── docker-compose.yml
├── Dockerfile
├── nginx.conf
└── entrypoint.sh
```

---

## Django-приложения

### accounts/
**Модели** (все `managed=False`, таблицы в БД управляются вне Django):

| Модель | Таблица | Описание |
|--------|---------|----------|
| `LookupRoleCode` | `lookup_role_codes` | Справочник ролей (PK: role_code) |
| `Counterparty` | `counterparties` | Контрагенты (UUID PK) |
| `Account` | `accounts` | Пользователи системы (UUID PK, permissions: ArrayField) |

**Ключевые файлы:**
- `accounts/backends.py` — `AccountsAuthBackend`: аутентификация через таблицу `accounts`, синхронизирует Django User для JWT
- `accounts/permissions.py` — `CanEditReferences`: единственная копия permission-класса (используется в accounts/ и reference/)

**Ключевые URLs** (`/api/accounts/`):
- `POST /login/` — JWT-токены
- `POST /logout/` — blacklist refresh
- `GET  /me/` — текущий пользователь
- `POST /register/` — регистрация
- `POST /set-password/` — установка пароля при первом входе
- `GET  /inn-lookup/` — DaData API (ИНН → данные компании)
- `POST /token/refresh/` — обновить access-токен
- `POST /token/verify/` — проверить токен
- `GET/POST/PATCH/DELETE /users/` — управление аккаунтами (admin only)
- `GET/POST/PATCH/DELETE /counterparties/` — управление контрагентами

### applications/
**Модели:**

| Модель | Описание |
|--------|----------|
| `Application` | Заявка (UUID PK, `managed=False`, таблица `applications`) |
| `InspectionRecord` | «Алан досмотра» — оперативный трекинг отгрузок (managed Django) |

**Application fields:** uuid, application_number, applicant_counterparty (FK), applicant_account (FK), terminal (FK), product (FK), power_of_attorney (FK), status_code, submitted_at, notes, is_active, created_at, updated_at

**Ключевые URLs** (`/api/`):
- `GET/POST /applications/`
- `GET/PUT/PATCH/DELETE /applications/{id}/`
- `POST /applications/{id}/change-status/` — смена status_code
- `GET /applications/{id}/files/` — список сгенерированных файлов (stub, возвращает [] до реализации Шаг 2)
- `GET/POST/PUT/DELETE /inspection-records/`

**Генерация документов:** `applications/document_generator.py` — `DocumentGenerator` (python-docx + openpyxl).
⚠️ **Не подключён к views.** Это запланированная функциональность (Шаг 2). Класс обращается к полям Application, которых пока нет в модели. Endpoint `generate_documents/` и `downloadFile` во frontend вызывают несуществующий backend — реализация отложена.

### reference/
**4 модели** (все `managed=False`):

| Модель | Таблица | Описание |
|--------|---------|----------|
| `LookupStatusCode` | — | Статусы заявок (read-only) |
| `Terminal` | — | Терминалы (с owner_counterparty FK) |
| `Product` | — | Продукция |
| `PowerOfAttorney` | — | Доверенности |

**Ключевые URLs** (`/api/reference/`):
- `GET /statuses/` — read-only список статусов
- `GET/POST/PATCH/DELETE /terminals/`
- `GET/POST/PATCH/DELETE /products/`
- `GET/POST/PATCH/DELETE /powers-of-attorney/`

Инициализация данных: `python manage.py init_data`

---

## Frontend (React + TypeScript)

**Зависимости:** React 18, React Router 6, Ant Design 5, Axios, Zustand, Dayjs (ru-locale).

### Маршруты (App.tsx)
| Путь | Компонент |
|------|-----------|
| `/` | AlanDosmotraPage (главная — план досмотра) |
| `/dashboard` | DashboardPage |
| `/applications` | ApplicationsListPage |
| `/applications/new` | ApplicationFormPage |
| `/applications/:id` | ApplicationFormPage (просмотр) |
| `/applications/:id/edit` | ApplicationFormPage (редактирование) |
| `/reference/counterparties` | CounterpartiesPage |
| `/reference/products` | ProductsPage |
| `/reference/terminals` | TerminalsPage |
| `/reference/powers-of-attorney` | PowersOfAttorneyPage |
| `/admin/users` | UsersPage |

### Ключевые файлы
| Файл | Роль |
|------|------|
| `frontend/src/api/axios.ts` | Axios instance + JWT interceptor + auto-refresh |
| `frontend/src/store/authStore.ts` | Zustand: токены, user, isAuthenticated → localStorage |
| `frontend/src/api/auth.ts` | login / logout / me / register / innLookup |
| `frontend/src/api/applications.ts` | CRUD заявок: list, get, create, update, remove, changeStatus, getFiles, generateDocuments, downloadFile |
| `frontend/src/api/reference.ts` | Все справочники |
| `frontend/src/api/inspectionRecords.ts` | CRUD AlanDosmotra |
| `frontend/src/types/application.ts` | Application, GeneratedFile, PaginatedResponse |
| `frontend/src/types/reference.ts` | Все справочные типы |
| `frontend/src/components/Layout/` | AppLayout, AppHeader, Sidebar |
| `frontend/src/components/ReferenceTable.tsx` | Переиспользуемая таблица справочников |

---

## Docker Compose — 5 сервисов

| Сервис | Образ / Build | Порт (host) |
|--------|---------------|-------------|
| `postgres` | postgres:15 | 5434→5432 |
| `pgadmin` | pgadmin4 | 5051→80 |
| `agrodb_web` | ./Dockerfile | (внутренний) |
| `agrodb_frontend` | ./frontend/Dockerfile | (внутренний) |
| `agrodb_nginx` | nginx | 80, 443 |

**БД:** user=postgres, password=12345, db=mydb  
**PgAdmin:** shaddar08@gmail.com

### Nginx routing
- `/static/` → Django (кэш 30д)
- `/media/` → Django (кэш 7д)
- `/api/` → Django (порт 8000)
- `/admin/` → Django admin
- `/files/` → file downloads
- `/` → React SPA (порт 80)

### Entrypoint порядок запуска
1. Ждёт PostgreSQL (`nc -z postgres 5432`)
2. `python manage.py migrate --noinput`
3. Создаёт superuser admin/admin123 (идемпотентно)
4. `python manage.py init_data` (справочники)
5. Запускает Gunicorn (3 workers)

---

## Django Settings (ключевые)

| Параметр | Значение |
|----------|---------|
| LANGUAGE_CODE | ru-ru |
| TIME_ZONE | Europe/Moscow |
| AUTH | JWT (simplejwt): access 8h, refresh 7d, rotate enabled |
| CORS | localhost:3000, localhost:5173 |
| DATABASES | PostgreSQL через dj-database-url |
| MAX_UPLOAD | 100M (nginx) |

---

## Локальный сервер (Docker)

- **IP сервера:** `192.168.1.155`
- Приложение доступно на `http://192.168.1.155` (Nginx, порт 80)
- PgAdmin: `http://192.168.1.155:5051`
- PostgreSQL: `192.168.1.155:5434`

---

## Быстрый справочник команд

```bash
# Локально (разработка)
cd frontend && npm run dev          # Vite dev-server :5173
python manage.py runserver          # Django :8000

# Docker (продакшн / сервер)
docker compose up -d --build        # Сборка и запуск
docker compose logs -f agrodb_web   # Логи бэкенда
docker compose exec agrodb_web python manage.py migrate
docker compose exec agrodb_web python manage.py init_data
docker compose exec agrodb_web python manage.py createsuperuser

# БД — резервная копия
docker compose exec postgres pg_dump -U postgres mydb > backup.sql
docker compose exec -T postgres psql -U postgres mydb < backup.sql
```

---

## Python-зависимости (requirements.txt)

```
Django==4.2.7
djangorestframework==3.14.0
djangorestframework-simplejwt==5.3.1
django-cors-headers==4.3.1
psycopg2-binary==2.9.9
dj-database-url==2.1.0
python-docx==1.1.0
openpyxl==3.1.2
Pillow==12.1.1
requests==2.32.3
```

---

## Архитектурные паттерны

**Backend:**
- `ModelViewSet` + кастомные сериализаторы per-action (`list` vs `detail` vs `create`)
- Все основные модели — `managed=False` (схема управляется вне Django ORM)
- `CanEditReferences` — единственная копия в `accounts/permissions.py`, используется и в `reference/`
- Фильтрация через query params: `status`, `search`, `date_from`, `date_to`, `active_only`

**Frontend:**
- JWT auto-refresh в Axios interceptor (не выбрасывает пользователя)
- Zustand persists в `localStorage` (key: `auth-storage`)
- `ReferenceTable` — универсальный компонент для всех справочников
- Строгий TypeScript (`strict: true`)

---

## Документация проекта

- `agro-inspection-db-project/PROJECT_BRIEF.md` — бизнес-требования
- `agro-inspection-db-project/api/*.md` — 9 файлов API-спецификации
- `agro-inspection-db-project/database/*.md` — 8 файлов схемы БД
