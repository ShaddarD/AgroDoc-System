export interface ApplicationStatus {
  id: string
  code: string
  name: string
  sort_order: number | null
}

export interface SenderRu {
  id: string
  name: string
  legal_address: string
  actual_address: string
  inn: string
  kpp: string
  ogrn: string
  is_active: boolean
}

export interface SenderPowerOfAttorney {
  id: string
  sender: string
  number: string
  date: string
  valid_from: string | null
  valid_to: string | null
  is_active: boolean
}

export interface Receiver {
  id: string
  name_en: string
  legal_address: string
  actual_address: string
  inn: string
  kpp: string
  ogrn: string
  is_active: boolean
}

export interface Gost {
  id: string
  code: string
  name: string
}

export interface TrTs {
  id: string
  code: string
  name: string
}

export interface TrTsSampling {
  id: string
  code: string
  name: string
}

export interface Product {
  id: string
  name_ru: string
  name_rus: string
  name_eng: string
  botanical_name: string
  tnved_code: string
  gost: string | null
  tr_ts: string | null
  tr_ts_sampling: string | null
  is_active: boolean
}

export interface Applicant {
  id: string
  name_rus: string
  name_eng: string
  legal_address: string
  actual_address: string
  inn: string
  kpp: string
  ogrn: string
  contact_person: string
  phone: string
  email: string
  is_active: boolean
}

export interface Importer {
  id: string
  name_eng: string
  address_eng: string
  country: string
  city: string
  is_active: boolean
}

export interface InspectionPlace {
  id: string
  name: string
  address: string
  is_active: boolean
}

export interface ProductPurpose {
  id: string
  name: string
}

export interface PackingType {
  id: string
  name: string
}

export interface Country {
  id: string
  name_ru: string
  name_en: string
  iso_code: string
}

export interface Representative {
  id: string
  full_name: string
  email: string
  phone: string
  company_name: string
}

export interface SamplingPlace {
  id: string
  name: string
  address: string
}

export interface Laboratory {
  id: string
  name: string
  short_name: string
}

export interface Certificate {
  id: string
  name: string
}

export interface Regulation {
  id: string
  name: string
  regulation_type: string
}
