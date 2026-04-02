import api from './axios'
import type {
  Application, GeneratedFile, PaginatedResponse,
  ApplicationContainer, ApplicationCertificate, ApplicationRegulation,
} from '../types/application'

export const applicationsApi = {
  list: (params?: Record<string, string>) =>
    api.get<PaginatedResponse<Application>>('/applications/', { params }),

  get: (id: string) =>
    api.get<Application>(`/applications/${id}/`),

  getByNumber: (number: string) =>
    api.get<Application>(`/applications/by-number/${number}/`),

  create: (data: Partial<Application>) =>
    api.post<Application>('/applications/', data),

  update: (id: string, data: Partial<Application>) =>
    api.patch<Application>(`/applications/${id}/`, data),

  remove: (id: string) =>
    api.delete(`/applications/${id}/`),

  changeStatus: (id: string, statusCode: string) =>
    api.post(`/applications/${id}/change-status/`, { status: statusCode }),

  // Containers
  listContainers: (id: string) =>
    api.get<ApplicationContainer[]>(`/applications/${id}/containers/`),

  addContainer: (id: string, data: Partial<ApplicationContainer>) =>
    api.post<ApplicationContainer>(`/applications/${id}/containers/`, data),

  updateContainer: (id: string, containerId: string, data: Partial<ApplicationContainer>) =>
    api.patch<ApplicationContainer>(`/applications/${id}/containers/${containerId}/`, data),

  removeContainer: (id: string, containerId: string) =>
    api.delete(`/applications/${id}/containers/${containerId}/`),

  // Certificates
  listCertificates: (id: string) =>
    api.get<ApplicationCertificate[]>(`/applications/${id}/certificates/`),

  addCertificate: (id: string, data: Partial<ApplicationCertificate>) =>
    api.post<ApplicationCertificate>(`/applications/${id}/certificates/`, data),

  updateCertificate: (id: string, certId: string, data: Partial<ApplicationCertificate>) =>
    api.patch<ApplicationCertificate>(`/applications/${id}/certificates/${certId}/`, data),

  removeCertificate: (id: string, certId: string) =>
    api.delete(`/applications/${id}/certificates/${certId}/`),

  // Regulations
  listRegulations: (id: string) =>
    api.get<ApplicationRegulation[]>(`/applications/${id}/regulations/`),

  addRegulation: (id: string, data: Partial<ApplicationRegulation>) =>
    api.post<ApplicationRegulation>(`/applications/${id}/regulations/`, data),

  updateRegulation: (id: string, regId: string, data: Partial<ApplicationRegulation>) =>
    api.patch<ApplicationRegulation>(`/applications/${id}/regulations/${regId}/`, data),

  removeRegulation: (id: string, regId: string) =>
    api.delete(`/applications/${id}/regulations/${regId}/`),

  // Files & documents
  generateDocuments: (id: string, docTypes: string[]) =>
    api.post<GeneratedFile[]>(`/applications/${id}/generate_documents/`, { doc_types: docTypes }),

  getFiles: (id: string) =>
    api.get<GeneratedFile[]>(`/applications/${id}/files/`),

  downloadFile: (fileId: string) =>
    api.get(`/files/${fileId}/download/`, { responseType: 'blob' }),

  // History
  getHistory: (id: string) =>
    api.get(`/applications/${id}/history/`),
}
