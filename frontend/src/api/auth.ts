import api from './axios'
import type { User } from '../types/auth'

export const authApi = {
  login: (username: string, password: string) =>
    api.post<{ access: string; refresh: string; user: User }>('/accounts/login/', { username, password }),

  logout: (refresh: string) =>
    api.post('/accounts/logout/', { refresh }),

  me: () =>
    api.get<User>('/accounts/me/'),

  register: (data: { username: string; password: string; email?: string }) =>
    api.post<{ access: string; refresh: string; user: User }>('/accounts/register/', data),

  getUsers: () =>
    api.get<User[]>('/accounts/users/'),

  createUser: (data: Partial<User> & { password: string }) =>
    api.post<User>('/accounts/users/', data),

  updateUser: (id: number, data: Partial<User>) =>
    api.patch<User>(`/accounts/users/${id}/`, data),

  deleteUser: (id: number) =>
    api.delete(`/accounts/users/${id}/`),
}
