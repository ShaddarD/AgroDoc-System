import { useNavigate, useLocation } from 'react-router-dom'
import { Menu } from 'antd'
import {
  FileTextOutlined,
  TeamOutlined,
  ShopOutlined,
  GlobalOutlined,
  EnvironmentOutlined,
  UserOutlined,
  TableOutlined,
} from '@ant-design/icons'

const menuItems = [
  { key: '/', icon: <TableOutlined />, label: 'План досмотров' },
  { key: '/applications', icon: <FileTextOutlined />, label: 'Заявки' },
  {
    key: 'reference',
    icon: <ShopOutlined />,
    label: 'Справочники',
    children: [
      { key: '/reference/applicants', icon: <TeamOutlined />, label: 'Заявители' },
      { key: '/reference/products', icon: <ShopOutlined />, label: 'Продукция' },
      { key: '/reference/importers', icon: <GlobalOutlined />, label: 'Импортёры' },
      { key: '/reference/inspection-places', icon: <EnvironmentOutlined />, label: 'Места досмотра' },
    ],
  },
  { key: '/admin/users', icon: <UserOutlined />, label: 'Пользователи' },
]

interface Props {
  onNavigate?: () => void
}

export default function Sidebar({ onNavigate }: Props) {
  const navigate = useNavigate()
  const location = useLocation()

  const selectedKey = location.pathname === '/' ? '/' : (
    menuItems.flatMap((i: any) => i.children || i).find((i: any) => location.pathname.startsWith(i.key) && i.key !== '/')?.key ?? location.pathname
  )

  return (
    <Menu
      theme="dark"
      mode="inline"
      selectedKeys={[selectedKey]}
      defaultOpenKeys={['reference']}
      items={menuItems}
      onClick={({ key }) => { navigate(key); onNavigate?.() }}
      style={{ border: 'none' }}
    />
  )
}
