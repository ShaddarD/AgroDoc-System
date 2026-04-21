import api from './axios'

export interface InspectionRecord {
  id?: number
  number: string
  client: string
  manager: string
  commodity: string
  container_count: string
  weight: string | null
  pod: string
  terminal: string
  quarantine: string
  inspection_date_plan: string | null
  fss_date_plan: string | null
  cargo_status: string
  documents_status: string
  comments: string
  application?: string | null
  application_number?: string | null
  created_at?: string
  updated_at?: string
}

export const inspectionRecordsApi = {
  list: (params?: Record<string, string>) =>
    api.get<InspectionRecord[]>('/inspection-records/', { params }),
  get: (id: number) =>
    api.get<InspectionRecord>(`/inspection-records/${id}/`),
  create: (data: Partial<InspectionRecord>) =>
    api.post<InspectionRecord>('/inspection-records/', data),
  update: (id: number, data: Partial<InspectionRecord>) =>
    api.patch<InspectionRecord>(`/inspection-records/${id}/`, data),
  remove: (id: number) =>
    api.delete(`/inspection-records/${id}/`),
}
