-- Migration: PowerOfAttorney refactor
--   1. validity_days → validity_years (с новой формулой GENERATED)
--   2. attorney_account_uuid (FK accounts) → attorney_counterparty_uuid (FK counterparties)
--
-- Apply: psql -U postgres mydb < migrations/poa_days_to_years.sql

BEGIN;

-- ── Блок 1: validity_days → validity_years ────────────────────────────────────

-- Убрать вычисляемую колонку (пересоздаём с новой формулой)
ALTER TABLE powers_of_attorney DROP COLUMN expiry_date;

-- Переименовать колонку
ALTER TABLE powers_of_attorney RENAME COLUMN validity_days TO validity_years;

-- Обновить CHECK-constraint
ALTER TABLE powers_of_attorney DROP CONSTRAINT IF EXISTS powers_of_attorney_validity_days_check;
ALTER TABLE powers_of_attorney ADD CONSTRAINT powers_of_attorney_validity_years_check
    CHECK (validity_years > 0);

-- МИГРАЦИЯ ДАННЫХ: конвертировать дни → годы (округлить, минимум 1)
-- Раскомментировать ТОЛЬКО если в таблице есть записи со старыми значениями в днях:
-- UPDATE powers_of_attorney
--     SET validity_years = GREATEST(1, ROUND(validity_years::numeric / 365)::integer);

-- Пересоздать generated-колонку с формулой в годах
ALTER TABLE powers_of_attorney
    ADD COLUMN expiry_date date
    GENERATED ALWAYS AS ((issue_date + (validity_years * interval '1 year'))::date) STORED;

-- ── Блок 2: attorney_account → attorney_counterparty ─────────────────────────

-- Снять старый FK-constraint на accounts
ALTER TABLE powers_of_attorney
    DROP CONSTRAINT IF EXISTS powers_of_attorney_attorney_account_uuid_fkey;

-- Переименовать колонку
ALTER TABLE powers_of_attorney
    RENAME COLUMN attorney_account_uuid TO attorney_counterparty_uuid;

-- Добавить новый FK-constraint на counterparties
ALTER TABLE powers_of_attorney
    ADD CONSTRAINT powers_of_attorney_attorney_counterparty_uuid_fkey
    FOREIGN KEY (attorney_counterparty_uuid)
    REFERENCES counterparties(uuid) ON DELETE RESTRICT;

COMMIT;
