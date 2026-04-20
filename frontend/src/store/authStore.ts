import { create } from 'zustand'
import type { User } from '../types/auth'

const INACTIVITY_MS = 15 * 60 * 1000

function isSessionExpired(): boolean {
  const last = localStorage.getItem('last_activity')
  if (!last) return false
  return Date.now() - parseInt(last) > INACTIVITY_MS
}

function loadUser(): User | null {
  if (isSessionExpired()) {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('auth_user')
    localStorage.removeItem('last_activity')
    return null
  }
  const raw = localStorage.getItem('auth_user')
  return raw ? JSON.parse(raw) : null
}

interface AuthState {
  user: User | null
  accessToken: string | null
  refreshToken: string | null
  isAuthenticated: boolean
  setAuth: (user: User, access: string, refresh: string) => void
  clearAuth: () => void
  setUser: (user: User) => void
}

const initialUser = loadUser()

export const useAuthStore = create<AuthState>(() => ({
  user: initialUser,
  accessToken: initialUser ? localStorage.getItem('access_token') : null,
  refreshToken: initialUser ? localStorage.getItem('refresh_token') : null,
  isAuthenticated: !!initialUser,

  setAuth: (user, access, refresh) => {
    localStorage.setItem('access_token', access)
    localStorage.setItem('refresh_token', refresh)
    localStorage.setItem('auth_user', JSON.stringify(user))
    localStorage.setItem('last_activity', Date.now().toString())
    useAuthStore.setState({ user, accessToken: access, refreshToken: refresh, isAuthenticated: true })
  },

  clearAuth: () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('auth_user')
    localStorage.removeItem('last_activity')
    useAuthStore.setState({ user: null, accessToken: null, refreshToken: null, isAuthenticated: false })
  },

  setUser: (user) => {
    localStorage.setItem('auth_user', JSON.stringify(user))
    useAuthStore.setState({ user })
  },
}))
