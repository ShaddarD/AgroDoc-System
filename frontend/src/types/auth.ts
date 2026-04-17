export interface User {
  id: number
  username: string
  email: string
  first_name: string
  last_name: string
  full_name: string
  patronymic: string
  company_name: string
  inn: string
  is_staff: boolean
  is_active: boolean
  is_superuser: boolean
  date_joined: string
}

export interface AuthTokens {
  access: string
  refresh: string
}
