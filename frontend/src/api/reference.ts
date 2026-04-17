import api from './axios'
import type {
  ApplicationStatus, SenderRu, SenderPowerOfAttorney, Receiver,
  Gost, TrTs, TrTsSampling, Product, ProductPurpose, PackingType,
  Country, Representative, SamplingPlace, Laboratory, Certificate, Regulation,
  Applicant, Importer, InspectionPlace,
} from '../types/reference'

const makeRefApi = <T>(path: string) => ({
  list: (params?: Record<string, string>) => api.get<T[]>(path, { params }),
  get: (id: string) => api.get<T>(`${path}${id}/`),
  create: (data: Partial<T>) => api.post<T>(path, data),
  update: (id: string, data: Partial<T>) => api.patch<T>(`${path}${id}/`, data),
  remove: (id: string) => api.delete(`${path}${id}/`),
})

export const statusesApi = makeRefApi<ApplicationStatus>('/reference/statuses/')
export const sendersApi = makeRefApi<SenderRu>('/reference/senders/')
export const powersOfAttorneyApi = makeRefApi<SenderPowerOfAttorney>('/reference/powers-of-attorney/')
export const receiversApi = makeRefApi<Receiver>('/reference/receivers/')
export const gostsApi = makeRefApi<Gost>('/reference/gosts/')
export const trTsApi = makeRefApi<TrTs>('/reference/tr-ts/')
export const trTsSamplingApi = makeRefApi<TrTsSampling>('/reference/tr-ts-sampling/')
export const productsApi = makeRefApi<Product>('/reference/products/')
export const purposesApi = makeRefApi<ProductPurpose>('/reference/purposes/')
export const packingTypesApi = makeRefApi<PackingType>('/reference/packing-types/')
export const countriesApi = makeRefApi<Country>('/reference/countries/')
export const representativesApi = makeRefApi<Representative>('/reference/representatives/')
export const samplingPlacesApi = makeRefApi<SamplingPlace>('/reference/sampling-places/')
export const laboratoriesApi = makeRefApi<Laboratory>('/reference/laboratories/')
export const certificatesApi = makeRefApi<Certificate>('/reference/certificates/')
export const regulationsApi = makeRefApi<Regulation>('/reference/regulations/')
export const applicantsApi = makeRefApi<Applicant>('/reference/applicants/')
export const importersApi = makeRefApi<Importer>('/reference/importers/')
export const inspectionPlacesApi = makeRefApi<InspectionPlace>('/reference/inspection-places/')
