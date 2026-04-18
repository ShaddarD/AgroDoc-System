import { useAuthStore } from '../store/authStore'

export function useCanEdit(): boolean {
  const { user } = useAuthStore()
  if (!user) return false
  return user.role_code === 'admin' || user.role_code === 'manager'
}

export function useCanAdd(): boolean {
  const { user } = useAuthStore()
  if (!user) return false
  return ['admin', 'manager', 'user'].includes(user.role_code)
}
