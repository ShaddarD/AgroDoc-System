import { useNavigate, useLocation } from 'react-router-dom'
import { Menu } from 'antd'
import {
  FileTextOutlined,
  TeamOutlined,
  ShopOutlined,
  EnvironmentOutlined,
  UserOutlined,
  TableOutlined,
  SafetyCertificateOutlined,
  SettingOutlined,
} from '@ant-design/icons'
import { useAuthStore } from '../../store/authStore'

interface Props {
  onNavigate?: () => void
}

export default function Sidebar({ onNavigate }: Props) {
  const navigate = useNavigate()
  const location = useLocation()
  const { user } = useAuthStore()
  const isAdmin = user?.role_code === 'admin'
  const isAuthenticated = !!user
  const canReference = isAdmin || !!(user?.permissions?.includes('reference'))

  const menuItems = [
    { key: '/', icon: <TableOutlined />, label: 'План досмотров' },
    ...(isAuthenticated ? [
      { key: '/applications', icon: <FileTextOutlined />, label: 'Заявки' },
      ...(canReference ? [{
        key: 'reference',
        icon: <ShopOutlined />,
        label: 'Справочники',
        children: [
          { key: '/reference/counterparties', icon: <TeamOutlined />, label: 'Контрагенты' },
          { key: '/reference/products', icon: <ShopOutlined />, label: 'Продукция' },
          { key: '/reference/terminals', icon: <EnvironmentOutlined />, label: 'Терминалы' },
          { key: '/reference/powers-of-attorney', icon: <SafetyCertificateOutlined />, label: 'Доверенности' },
        ],
      }] : []),
    ] : []),
    ...(isAdmin ? [
      {
        key: 'admin',
        icon: <SettingOutlined />,
        label: 'Администрирование',
        children: [
          { key: '/manage/users', icon: <UserOutlined />, label: 'Пользователи' },
        ],
      },
    ] : []),
  ]

  const allLeafKeys = menuItems.flatMap((i: any) =>
    i.children ? i.children.flatMap((c: any) => c.children || c) : [i]
  )
  const selectedKey = location.pathname === '/'
    ? '/'
    : allLeafKeys.find((i: any) => location.pathname.startsWith(i.key) && i.key !== '/')?.key ?? location.pathname

  return (
    <Menu
      theme="dark"
      mode="inline"
      selectedKeys={[selectedKey]}
      defaultOpenKeys={['reference', 'admin']}
      items={menuItems}
      onClick={({ key }) => { navigate(key); onNavigate?.() }}
      style={{ border: 'none' }}
    />
  )
}
