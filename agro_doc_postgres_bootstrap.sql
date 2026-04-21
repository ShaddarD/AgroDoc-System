-- Agro Doc PostgreSQL bootstrap script
-- Purpose:
--   1) Fully reset the CURRENT database schema
--   2) Recreate lookup tables and business tables
--   3) Add constraints, indexes, triggers

BEGIN;

CREATE EXTENSION IF NOT EXISTS pgcrypto;

DROP SCHEMA IF EXISTS public CASCADE;
CREATE SCHEMA public;
GRANT ALL ON SCHEMA public TO CURRENT_USER;
GRANT ALL ON SCHEMA public TO public;

CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- =========================================================
-- Utility trigger for updated_at
-- =========================================================
CREATE OR REPLACE FUNCTION set_updated_at()
RETURNS trigger AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- =========================================================
-- Lookup tables
-- =========================================================
CREATE TABLE lookup_role_codes (
  role_code        varchar(50) PRIMARY KEY,
  display_name_ru  varchar(100) NOT NULL,
  display_name_en  varchar(100)
);

CREATE TABLE lookup_status_codes (
  status_code      varchar(50) PRIMARY KEY,
  description      varchar(255) NOT NULL
);

INSERT INTO lookup_role_codes (role_code, display_name_ru, display_name_en) VALUES
  ('admin',   'Администратор', 'Administrator'),
  ('manager', 'Менеджер',      'Manager'),
  ('user',    'Пользователь',  'User');

INSERT INTO lookup_status_codes (status_code, description) VALUES
  ('active',   'Active / valid'),
  ('inactive', 'Inactive'),
  ('blocked',  'Blocked'),
  ('revoked',  'Revoked'),
  ('draft',    'Draft / pending');

-- =========================================================
-- Main business tables
-- =========================================================
CREATE TABLE counterparties (
  uuid                uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  name_ru             varchar(255) NOT NULL,
  name_en             varchar(255),
  inn                 varchar(12),
  kpp                 varchar(9),
  ogrn                varchar(15),
  legal_address_ru    text,
  actual_address_ru   text,
  legal_address_en    text,
  actual_address_en   text,
  status_code         varchar(50) NOT NULL DEFAULT 'active' REFERENCES lookup_status_codes(status_code),
  is_active           boolean NOT NULL DEFAULT true,
  created_at          timestamptz NOT NULL DEFAULT NOW(),
  updated_at          timestamptz NOT NULL DEFAULT NOW(),

  CONSTRAINT uq_counterparties_inn_kpp UNIQUE (inn, kpp),
  CONSTRAINT chk_counterparties_inn_len CHECK (inn IS NULL OR char_length(inn) IN (10, 12)),
  CONSTRAINT chk_counterparties_kpp_len CHECK (kpp IS NULL OR char_length(kpp) = 9),
  CONSTRAINT chk_counterparties_ogrn_len CHECK (ogrn IS NULL OR char_length(ogrn) IN (13, 15))
);

CREATE TABLE accounts (
  uuid                uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  login               varchar(100) NOT NULL UNIQUE,
  password_hash       text NOT NULL,
  role_code           varchar(50) NOT NULL REFERENCES lookup_role_codes(role_code),
  last_name           varchar(100) NOT NULL,
  first_name          varchar(100) NOT NULL,
  middle_name         varchar(100),
  counterparty_uuid   uuid REFERENCES counterparties(uuid) ON DELETE SET NULL,
  phone               varchar(32),
  email               varchar(255),
  job_title           varchar(150),
  is_active           boolean NOT NULL DEFAULT true,
  created_at          timestamptz NOT NULL DEFAULT NOW(),
  updated_at          timestamptz NOT NULL DEFAULT NOW(),

  CONSTRAINT uq_accounts_email UNIQUE (email),
  CONSTRAINT chk_accounts_email_lower CHECK (email IS NULL OR email = lower(email))
);

CREATE TABLE terminals (
  uuid                    uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  terminal_code           varchar(50) NOT NULL UNIQUE,
  terminal_name           varchar(255) NOT NULL,
  owner_counterparty_uuid uuid REFERENCES counterparties(uuid) ON DELETE SET NULL,
  address_ru              text NOT NULL,
  address_en              text,
  is_active               boolean NOT NULL DEFAULT true,
  created_at              timestamptz NOT NULL DEFAULT NOW(),
  updated_at              timestamptz NOT NULL DEFAULT NOW()
);

CREATE TABLE products (
  uuid                   uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  product_code           varchar(50) NOT NULL UNIQUE,
  hs_code_tnved          varchar(20) NOT NULL,
  name_ru                varchar(255) NOT NULL,
  name_en                varchar(255),
  botanical_name_latin   varchar(255),
  regulatory_documents   text,
  is_active              boolean NOT NULL DEFAULT true,
  created_at             timestamptz NOT NULL DEFAULT NOW(),
  updated_at             timestamptz NOT NULL DEFAULT NOW(),

  CONSTRAINT chk_products_hs_code_digits CHECK (hs_code_tnved ~ '^[0-9]+$')
);

CREATE TABLE powers_of_attorney (
  uuid                         uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  poa_number                   varchar(100) NOT NULL,
  issue_date                   date NOT NULL,
  validity_years               integer NOT NULL CHECK (validity_years > 0),
  expiry_date                  date GENERATED ALWAYS AS ((issue_date + (validity_years * interval '1 year'))::date) STORED,
  principal_counterparty_uuid  uuid REFERENCES counterparties(uuid) ON DELETE RESTRICT,
  attorney_counterparty_uuid   uuid REFERENCES counterparties(uuid) ON DELETE RESTRICT,
  status_code                  varchar(50) NOT NULL DEFAULT 'active' REFERENCES lookup_status_codes(status_code),
  is_active                    boolean NOT NULL DEFAULT true,
  created_at                   timestamptz NOT NULL DEFAULT NOW(),
  updated_at                   timestamptz NOT NULL DEFAULT NOW(),

  CONSTRAINT uq_poa_number_issue_date UNIQUE (poa_number, issue_date)
);

CREATE TABLE applications (
  uuid                         uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  application_number           varchar(100) UNIQUE,
  applicant_counterparty_uuid  uuid REFERENCES counterparties(uuid) ON DELETE RESTRICT,
  applicant_account_uuid       uuid REFERENCES accounts(uuid) ON DELETE RESTRICT,
  terminal_uuid                uuid REFERENCES terminals(uuid) ON DELETE RESTRICT,
  product_uuid                 uuid REFERENCES products(uuid) ON DELETE RESTRICT,
  power_of_attorney_uuid       uuid REFERENCES powers_of_attorney(uuid) ON DELETE SET NULL,
  status_code                  varchar(50) NOT NULL DEFAULT 'draft' REFERENCES lookup_status_codes(status_code),
  submitted_at                 timestamptz,
  notes                        text,
  is_active                    boolean NOT NULL DEFAULT true,
  created_at                   timestamptz NOT NULL DEFAULT NOW(),
  updated_at                   timestamptz NOT NULL DEFAULT NOW()
);

-- =========================================================
-- Indexes
-- =========================================================
CREATE INDEX idx_accounts_counterparty_uuid ON accounts(counterparty_uuid);
CREATE INDEX idx_accounts_role_code ON accounts(role_code);
CREATE INDEX idx_terminals_owner_counterparty_uuid ON terminals(owner_counterparty_uuid);
CREATE INDEX idx_products_hs_code_tnved ON products(hs_code_tnved);
CREATE INDEX idx_poa_principal_counterparty_uuid ON powers_of_attorney(principal_counterparty_uuid);
CREATE INDEX idx_poa_attorney_account_uuid ON powers_of_attorney(attorney_account_uuid);
CREATE INDEX idx_poa_status_code ON powers_of_attorney(status_code);
CREATE INDEX idx_counterparties_status_code ON counterparties(status_code);
CREATE INDEX idx_applications_applicant_counterparty_uuid ON applications(applicant_counterparty_uuid);
CREATE INDEX idx_applications_applicant_account_uuid ON applications(applicant_account_uuid);
CREATE INDEX idx_applications_terminal_uuid ON applications(terminal_uuid);
CREATE INDEX idx_applications_product_uuid ON applications(product_uuid);
CREATE INDEX idx_applications_power_of_attorney_uuid ON applications(power_of_attorney_uuid);
CREATE INDEX idx_applications_status_code ON applications(status_code);

-- =========================================================
-- Triggers
-- =========================================================
CREATE TRIGGER trg_counterparties_updated_at
BEFORE UPDATE ON counterparties
FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE TRIGGER trg_accounts_updated_at
BEFORE UPDATE ON accounts
FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE TRIGGER trg_terminals_updated_at
BEFORE UPDATE ON terminals
FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE TRIGGER trg_products_updated_at
BEFORE UPDATE ON products
FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE TRIGGER trg_powers_of_attorney_updated_at
BEFORE UPDATE ON powers_of_attorney
FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE TRIGGER trg_applications_updated_at
BEFORE UPDATE ON applications
FOR EACH ROW EXECUTE FUNCTION set_updated_at();

COMMIT;
