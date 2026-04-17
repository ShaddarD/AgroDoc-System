# AgroDoc-System — Master Project File

## Назначение системы
Система автоматизации оформления заявок на инспекцию/досмотр/сертификацию сельскохозяйственной продукции.  
**Стек:** Django 4.2 (DRF) + React 18 (TypeScript, Ant Design v5) + PostgreSQL 15 + Docker Compose.

---

## Структура монорепо

```
AgroDoc-System/
├── agro_doc/          # Django project root (settings, urls)
├── accounts/          # Пользователи и JWT-аутентификация
├── applications/      # Основная бизнес-логика (заявки, досмотры, генерация документов)
├── reference/         # Справочники (17 моделей)
├── frontend/          # React SPA
├── templates/         # Django-шаблоны (admin, документы)
├── media/             # Сгенерированные файлы и загрузки
├── agro-inspection-db-project/  # Проектная документация (API + DB specs)
├── docker-compose.yml
├── Dockerfile
├── nginx.conf
└── entrypoint.sh
```

---

## Django-приложения

### accounts/
- **Модель:** `UserProfile` — расширение User (отчество, компания, ИНН)
- **Ключевые URLs:**
  - `POST /api/accounts/login/` — JWT-токены
  - `POST /api/accounts/logout/` — blacklist refresh
  - `GET  /api/accounts/me/` — текущий пользователь
  - `POST /api/accounts/register/` — только admin
  - `GET  /api/accounts/inn-lookup/` — DaData API (ИНН → данные компании)
  - `POST /api/accounts/token/refresh/` — обновить access-токен

### applications/
**Модели:**
| Модель | Описание |
|--------|----------|
| `Application` | Заявка (UUID PK, автономер, статус, FK на 10+ справочников) |
| `ApplicationContainer` | 1-to-many: номера контейнеров |
| `ApplicationCertificate` | 1-to-many: требуемые сертификаты |
| `ApplicationRegulation` | 1-to-many: нормативные документы |
| `GeneratedFile` | Сгенерированные DOCX/XLSX файлы |
| `InspectionRecord` | «Алан досмотра» — оперативный учёт отгрузок |
| `ApplicationHistory` | Журнал изменений (JSONField) |

**Ключевые URLs:**
- `GET/POST /api/applications/`
- `GET/PUT/PATCH/DELETE /api/applications/{id}/`
- `GET/POST /api/applications/{id}/containers/`
- `GET/POST /api/applications/{id}/certificates/`
- `GET/POST /api/applications/{id}/regulations/`
- `POST /api/applications/{id}/generate-documents/` — генерация DOCX/XLSX
- `GET/POST /api/applications/inspection-records/`

**Генерация документов:** `applications/document_generator.py` — `DocumentGenerator` (python-docx + openpyxl).

### reference/
17 справочных моделей: `ApplicationStatus`, `SenderRu`, `SenderPowerOfAttorney`, `Receiver`, `Gost`, `TrTs`, `TrTsSampling`, `Product`, `ProductPurpose`, `PackingType`, `Country`, `Representative`, `SamplingPlace`, `Laboratory`, `Certificate`, `Regulation`.

Инициализация: `python manage.py init_data`

---

## Frontend (React + TypeScript)

**Зависимости:** React 18, React Router 6, Ant Design 5, Axios, Zustand, Dayjs (ru-locale).

### Маршруты (App.tsx)
| Путь | Компонент |
|------|-----------|
| `/login` | LoginPage |
| `/` | AlanDosmotraPage (индекс) |
| `/dashboard` | DashboardPage |
| `/applications` | ApplicationsListPage |
| `/applications/new` | ApplicationFormPage |
| `/applications/:id` | ApplicationFormPage (просмотр) |
| `/applications/:id/edit` | ApplicationFormPage (редактирование) |
| `/reference/applicants` | ApplicantsPage |
| `/reference/products` | ProductsPage |
| `/reference/importers` | ImportersPage |
| `/reference/inspection-places` | InspectionPlacesPage |
| `/admin/users` | UsersPage |

### Ключевые файлы
| Файл | Роль |
|------|------|
| `frontend/src/api/axios.ts` | Axios instance + JWT interceptor + auto-refresh |
| `frontend/src/store/authStore.ts` | Zustand: токены, user, isAuthenticated → localStorage |
| `frontend/src/api/auth.ts` | login / logout / me / register / innLookup |
| `frontend/src/api/applications.ts` | CRUD заявок + контейнеры/сертификаты/документы |
| `frontend/src/api/reference.ts` | Все справочники |
| `frontend/src/api/inspectionRecords.ts` | CRUD AlDosmotra |
| `frontend/src/types/application.ts` | Application, Container, Certificate, Regulation, GeneratedFile |
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
- Вложенные маршруты для дочерних записей
- Фильтрация через query params: `status`, `search`, `date_from`, `date_to`
- `ApplicationHistory` — JSONField audit log

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
