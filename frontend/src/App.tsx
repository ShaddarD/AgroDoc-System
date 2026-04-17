import { ConfigProvider } from 'antd'
import ruRU from 'antd/locale/ru_RU'
import dayjs from 'dayjs'
import 'dayjs/locale/ru'
import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom'
import theme from './theme'
import PrivateRoute from './components/PrivateRoute'
import AppLayout from './components/Layout/AppLayout'
import PublicPlanLayout from './components/Layout/PublicPlanLayout'
import LoginPage from './pages/Login/LoginPage'
import DashboardPage from './pages/Dashboard/DashboardPage'
import ApplicationsListPage from './pages/Applications/ApplicationsListPage'
import ApplicationFormPage from './pages/Applications/ApplicationFormPage'
import ApplicantsPage from './pages/Reference/ApplicantsPage'
import ProductsPage from './pages/Reference/ProductsPage'
import ImportersPage from './pages/Reference/ImportersPage'
import InspectionPlacesPage from './pages/Reference/InspectionPlacesPage'
import UsersPage from './pages/Admin/UsersPage'

dayjs.locale('ru')

export default function App() {
  return (
    <ConfigProvider theme={theme} locale={ruRU}>
      <BrowserRouter>
        <Routes>
          {/* Публичный маршрут — всегда доступен */}
          <Route path="/" element={<PublicPlanLayout />} />

          <Route path="/login" element={<LoginPage />} />

          {/* Защищённые маршруты */}
          <Route element={<PrivateRoute><AppLayout /></PrivateRoute>}>
            <Route path="/dashboard" element={<DashboardPage />} />
            <Route path="/applications" element={<ApplicationsListPage />} />
            <Route path="/applications/new" element={<ApplicationFormPage />} />
            <Route path="/applications/:id" element={<ApplicationFormPage />} />
            <Route path="/applications/:id/edit" element={<ApplicationFormPage />} />
            <Route path="/reference/applicants" element={<ApplicantsPage />} />
            <Route path="/reference/products" element={<ProductsPage />} />
            <Route path="/reference/importers" element={<ImportersPage />} />
            <Route path="/reference/inspection-places" element={<InspectionPlacesPage />} />
            <Route path="/admin/users" element={<UsersPage />} />
          </Route>

          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </ConfigProvider>
  )
}
