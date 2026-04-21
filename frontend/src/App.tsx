import { useEffect } from 'react'
import { ConfigProvider } from 'antd'
import ruRU from 'antd/locale/ru_RU'
import dayjs from 'dayjs'
import 'dayjs/locale/ru'
import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom'
import theme from './theme'
import AppLayout from './components/Layout/AppLayout'
import DashboardPage from './pages/Dashboard/DashboardPage'
import AlanDosmotraPage from './pages/AlanDosmotra/AlanDosmotraPage'
import ApplicationsListPage from './pages/Applications/ApplicationsListPage'
import ApplicationFormPage from './pages/Applications/ApplicationFormPage'
import CounterpartiesPage from './pages/Reference/CounterpartiesPage'
import ProductsPage from './pages/Reference/ProductsPage'
import TerminalsPage from './pages/Reference/TerminalsPage'
import PowersOfAttorneyPage from './pages/Reference/PowersOfAttorneyPage'
import UsersPage from './pages/Admin/UsersPage'
import { useAuthStore } from './store/authStore'
import { authApi } from './api/auth'

dayjs.locale('ru')

export default function App() {
  const { isAuthenticated, setUser, clearAuth } = useAuthStore()

  // Restore user from server on app load (validates token, refreshes user data)
  useEffect(() => {
    if (isAuthenticated) {
      authApi.me()
        .then(({ data }) => setUser(data))
        .catch(() => clearAuth())
    }
  }, [])

  // Update last_activity on any user interaction (throttled to once per 30s)
  useEffect(() => {
    let lastUpdate = 0
    const update = () => {
      const now = Date.now()
      if (now - lastUpdate > 30_000 && localStorage.getItem('access_token')) {
        lastUpdate = now
        localStorage.setItem('last_activity', now.toString())
      }
    }
    window.addEventListener('mousemove', update)
    window.addEventListener('keydown', update)
    window.addEventListener('click', update)
    return () => {
      window.removeEventListener('mousemove', update)
      window.removeEventListener('keydown', update)
      window.removeEventListener('click', update)
    }
  }, [])

  return (
    <ConfigProvider theme={theme} locale={ruRU}>
      <BrowserRouter>
        <Routes>
          <Route element={<AppLayout />}>
            <Route path="/" element={<AlanDosmotraPage />} />
            <Route path="/dashboard" element={<DashboardPage />} />
            <Route path="/applications" element={<ApplicationsListPage />} />
            <Route path="/applications/new" element={<ApplicationFormPage />} />
            <Route path="/applications/:id" element={<ApplicationFormPage />} />
            <Route path="/applications/:id/edit" element={<ApplicationFormPage />} />
            <Route path="/reference/counterparties" element={<CounterpartiesPage />} />
            <Route path="/reference/products" element={<ProductsPage />} />
            <Route path="/reference/terminals" element={<TerminalsPage />} />
            <Route path="/reference/powers-of-attorney" element={<PowersOfAttorneyPage />} />
            <Route path="/manage/users" element={<UsersPage />} />
          </Route>

          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </ConfigProvider>
  )
}
