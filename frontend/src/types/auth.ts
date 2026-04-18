export interface Counterparty {
  uuid: string
  name_ru: string
  name_en: string | null
  inn: string | null
  kpp: string | null
}

export interface User {
  uuid: string
  login: string
  role_code: 'admin' | 'manager' | 'user' | string
  last_name: string
  first_name: string
  middle_name: string | null
  counterparty: Counterparty | null
  phone: string | null
  email: string | null
  job_title: string | null
  permissions: string[]
  is_active: boolean
}

export interface AuthTokens {
  access: string
  refresh: string
}

export type LoginResponse =
  | { success: true; access: string; refresh: string; user: User }
  | { needs_password_setup: true; account_uuid: string }
