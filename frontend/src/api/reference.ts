import api from './axios'
import type { Counterparty, Terminal, Product, PowerOfAttorney } from '../types/reference'

const makeRefApi = <T>(path: string) => ({
  list: (params?: Record<string, string>) => api.get<T[]>(path, { params }),
  get: (uuid: string) => api.get<T>(`${path}${uuid}/`),
  create: (data: Partial<T>) => api.post<T>(path, data),
  update: (uuid: string, data: Partial<T>) => api.patch<T>(`${path}${uuid}/`, data),
  remove: (uuid: string) => api.delete(`${path}${uuid}/`),
})

export const counterpartiesApi = makeRefApi<Counterparty>('/accounts/counterparties/')
export const terminalsApi = makeRefApi<Terminal>('/reference/terminals/')
export const productsApi = makeRefApi<Product>('/reference/products/')
export const powersOfAttorneyApi = makeRefApi<PowerOfAttorney>('/reference/powers-of-attorney/')
