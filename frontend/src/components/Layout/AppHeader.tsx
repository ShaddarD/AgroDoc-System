import { Avatar, Button, Dropdown, Space, Typography } from 'antd'
import { UserOutlined, LogoutOutlined, SettingOutlined, MenuOutlined } from '@ant-design/icons'
import { useNavigate } from 'react-router-dom'
import { useAuthStore } from '../../store/authStore'
import { authApi } from '../../api/auth'

interface Props {
  onMenuToggle?: () => void
}

export default function AppHeader({ onMenuToggle }: Props) {
  const navigate = useNavigate()
  const { user, refreshToken, clearAuth } = useAuthStore()

  const handleLogout = async () => {
    try {
      if (refreshToken) await authApi.logout(refreshToken)
    } catch { /* ignore */ }
    clearAuth()
    navigate('/login')
  }

  const menuItems = [
    {
      key: 'username',
      label: <Typography.Text type="secondary">{user?.username}</Typography.Text>,
      disabled: true,
    },
    { type: 'divider' as const },
    user?.is_staff
      ? { key: 'users', icon: <SettingOutlined />, label: 'Пользователи', onClick: () => navigate('/admin/users') }
      : null,
    { key: 'logout', icon: <LogoutOutlined />, label: 'Выйти', danger: true, onClick: handleLogout },
  ].filter(Boolean)

  return (
    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', height: '100%', padding: '0 16px' }}>
      <Space>
        {onMenuToggle && (
          <Button type="text" icon={<MenuOutlined />} onClick={onMenuToggle} />
        )}
        <Typography.Text strong style={{ fontSize: 16, color: '#1a3c6e' }}>
          AgroDoc Systems
        </Typography.Text>
      </Space>
      <Dropdown menu={{ items: menuItems }} placement="bottomRight">
        <Button type="text" style={{ height: 'auto', padding: '4px 8px' }}>
          <Space>
            <Avatar size="small" icon={<UserOutlined />} style={{ backgroundColor: '#1a3c6e' }} />
            <span>{user?.first_name || user?.username}</span>
          </Space>
        </Button>
      </Dropdown>
    </div>
  )
}
