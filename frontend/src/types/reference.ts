// ─── Lookup tables ────────────────────────────────────────────────────────────

export interface LookupStatusCode {
  status_code: string
  description: string
}

// ─── Main reference tables ────────────────────────────────────────────────────

export interface Counterparty {
  uuid: string
  name_ru: string
  name_en: string | null
  inn: string | null
  kpp: string | null
  ogrn: string | null
  legal_address_ru: string | null
  actual_address_ru: string | null
  legal_address_en: string | null
  actual_address_en: string | null
  status_code: string
  is_active: boolean
  created_at?: string
  updated_at?: string
}

export interface Terminal {
  uuid: string
  terminal_code: string
  terminal_name: string
  owner_counterparty: string | null
  owner_counterparty_name: string | null
  address_ru: string
  address_en: string | null
  is_active: boolean
  created_at?: string
  updated_at?: string
}

export interface Product {
  uuid: string
  product_code: string
  hs_code_tnved: string
  name_ru: string
  name_en: string | null
  botanical_name_latin: string | null
  regulatory_documents: string | null
  is_active: boolean
  created_at?: string
  updated_at?: string
}

export interface PowerOfAttorney {
  uuid: string
  poa_number: string
  issue_date: string
  validity_years: number
  expiry_date: string | null
  principal_counterparty: string | null
  principal_counterparty_name: string | null
  attorney_counterparty: string | null
  attorney_counterparty_name: string | null
  status_code: string
  is_active: boolean
  created_at?: string
  updated_at?: string
}

// Legacy types — kept for compatibility with ApplicationFormPage until it's updated
export interface ApplicationStatus { id: string; code: string; name: string }
export interface SenderRu { id: string; name: string; inn: string; kpp: string }
export interface SenderPowerOfAttorney { id: string; number: string; date: string }
export interface Receiver { id: string; name_en: string }
export interface Gost { id: string; code: string; name: string }
export interface TrTs { id: string; code: string; name: string }
export interface TrTsSampling { id: string; code: string; name: string }
export interface ProductPurpose { id: string; name: string }
export interface PackingType { id: string; name: string }
export interface Country { id: string; name_ru: string; name_en: string; iso_code: string }
export interface Representative { id: string; full_name: string }
export interface SamplingPlace { id: string; name: string }
export interface Laboratory { id: string; name: string }
export interface Certificate { id: string; name: string }
export interface Regulation { id: string; name: string }
export interface Applicant { id: string; name_rus: string; inn: string; is_active: boolean }
export interface Importer { id: string; name_eng: string; is_active: boolean }
export interface InspectionPlace { id: string; name: string; is_active: boolean }
