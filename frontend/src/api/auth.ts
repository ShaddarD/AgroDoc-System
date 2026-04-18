import api from './axios'
import type { User, LoginResponse } from '../types/auth'

interface RegisterData {
  login: string
  password: string
  password_confirm: string
  last_name: string
  first_name: string
  middle_name?: string
  email?: string
  phone?: string
  job_title?: string
  counterparty: string
}

interface CreateUserData {
  login: string
  password?: string
  role_code: string
  first_name: string
  last_name: string
  middle_name?: string
  email?: string
  phone?: string
  job_title?: string
  counterparty: string
}

interface AuthSuccess {
  success: true
  access: string
  refresh: string
  user: User
}

export const authApi = {
  login: (username: string, password: string) =>
    api.post<LoginResponse>('/accounts/login/', { username, password }),

  register: (data: RegisterData) =>
    api.post<AuthSuccess>('/accounts/register/', data),

  setPassword: (uuid: string, password: string) =>
    api.post<AuthSuccess>('/accounts/set-password/', {
      uuid,
      password,
      password_confirm: password,
    }),

  logout: (refresh: string) =>
    api.post('/accounts/logout/', { refresh }),

  me: () =>
    api.get<User>('/accounts/me/'),

  getUsers: () =>
    api.get<User[]>('/accounts/users/'),

  createUser: (data: CreateUserData) =>
    api.post<User>('/accounts/users/', data),

  updateUser: (uuid: string, data: Partial<CreateUserData> & { is_active?: boolean }) =>
    api.patch<User>(`/accounts/users/${uuid}/`, data),

  deleteUser: (uuid: string) =>
    api.delete(`/accounts/users/${uuid}/`),
}
