import type {
  ApplicationStatus, SenderRu, SenderPowerOfAttorney, Receiver,
  Product, ProductPurpose, PackingType, Country, Representative,
  SamplingPlace, Laboratory, Certificate, Regulation,
} from './reference'

export type FileType = 'cokz' | 'fito1' | 'fito2' | 'act' | 'other'

export interface ApplicationContainer {
  id: string
  container_number: string
  sort_order: number | null
}

export interface ApplicationCertificate {
  id: string
  certificate: string
  certificate_detail?: Certificate
  copies_count: number | null
  is_required: boolean | null
}

export interface ApplicationRegulation {
  id: string
  regulation: string
  regulation_detail?: Regulation
  comment: string
}

export interface Application {
  id: string
  application_number: string
  created_at: string
  updated_at: string
  created_by: number | null
  created_by_name?: string

  // Status
  status: string | null
  status_detail?: ApplicationStatus
  status_name?: string
  status_code?: string

  // Sender
  sender_ru: string | null
  sender_ru_detail?: SenderRu
  sender_power_of_attorney: string | null
  sender_power_of_attorney_detail?: SenderPowerOfAttorney
  sender_en_manual: string

  // Receiver
  receiver: string | null
  receiver_detail?: Receiver

  // Product
  product: string | null
  product_detail?: Product
  product_name_en_manual: string
  harvest_year: number | null
  manufacture_date: string | null
  purpose: string | null
  purpose_detail?: ProductPurpose

  // Shipping
  weight_mt: string | null
  packing_type: string | null
  packing_type_detail?: PackingType
  import_country: string | null
  import_country_detail?: Country
  discharge_port_ru_manual: string
  discharge_port_en_manual: string
  additional_declaration: string

  // Inspection
  representative: string | null
  representative_detail?: Representative
  sampling_place: string | null
  sampling_place_detail?: SamplingPlace
  laboratory: string | null
  laboratory_detail?: Laboratory

  // Contract & planning
  contract_number_manual: string
  contract_date_manual: string | null
  planned_inspection_date: string | null

  // Nested children (from detail endpoint)
  containers?: ApplicationContainer[]
  certificates?: ApplicationCertificate[]
  regulations?: ApplicationRegulation[]
}

export interface GeneratedFile {
  id: string
  application: string
  file_name: string
  file_path: string
  file_type: FileType
  created_at: string
  created_by: number | null
}

export interface PaginatedResponse<T> {
  count: number
  next: string | null
  previous: string | null
  results: T[]
}
