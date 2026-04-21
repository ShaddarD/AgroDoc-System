import api from './axios'
import type {
  Application, GeneratedFile, PaginatedResponse,
} from '../types/application'

export const applicationsApi = {
  list: (params?: Record<string, string>) =>
    api.get<PaginatedResponse<Application>>('/applications/', { params }),

  get: (id: string) =>
    api.get<Application>(`/applications/${id}/`),

  create: (data: Partial<Application>) =>
    api.post<Application>('/applications/', data),

  update: (id: string, data: Partial<Application>) =>
    api.patch<Application>(`/applications/${id}/`, data),

  remove: (id: string) =>
    api.delete(`/applications/${id}/`),

  changeStatus: (id: string, statusCode: string) =>
    api.post(`/applications/${id}/change-status/`, { status: statusCode }),

  generateDocuments: (id: string, docTypes: string[]) =>
    api.post<GeneratedFile[]>(`/applications/${id}/generate_documents/`, { doc_types: docTypes }),

  getFiles: (id: string) =>
    api.get<GeneratedFile[]>(`/applications/${id}/files/`),

  downloadFile: (fileId: string) =>
    api.get(`/files/${fileId}/download/`, { responseType: 'blob' }),
}
