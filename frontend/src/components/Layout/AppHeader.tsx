import { useState } from 'react'
import { Avatar, Button, Dropdown, Space, Typography, message } from 'antd'
import { MenuOutlined, LogoutOutlined, UserOutlined } from '@ant-design/icons'
import { useAuthStore } from '../../store/authStore'
import { authApi } from '../../api/auth'
import LoginModal from '../Auth/LoginModal'

interface Props {
  onMenuToggle?: () => void
}

export default function AppHeader({ onMenuToggle }: Props) {
  const { isAuthenticated, user, refreshToken, clearAuth } = useAuthStore()
  const [loginOpen, setLoginOpen] = useState(false)

  const handleLogout = async () => {
    try {
      if (refreshToken) await authApi.logout(refreshToken)
    } catch { /* ignore */ }
    clearAuth()
    message.success('Вы вышли из системы')
  }

  const initials = user
    ? `${user.first_name?.[0] ?? ''}${user.last_name?.[0] ?? ''}`.toUpperCase() || user.login[0].toUpperCase()
    : ''

  const userMenuItems = [
    {
      key: 'name',
      label: (
        <Typography.Text type="secondary">
          {user ? `${user.last_name} ${user.first_name}` : ''}
        </Typography.Text>
      ),
      disabled: true,
    },
    {
      key: 'login',
      label: <Typography.Text type="secondary">{user?.login}</Typography.Text>,
      disabled: true,
    },
    { type: 'divider' as const },
    {
      key: 'logout',
      icon: <LogoutOutlined />,
      label: 'Выйти',
      danger: true,
      onClick: handleLogout,
    },
  ]

  return (
    <div style={{
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      height: '100%',
      padding: '0 16px',
    }}>
      <Space>
        {onMenuToggle && (
          <Button type="text" icon={<MenuOutlined />} onClick={onMenuToggle} />
        )}
        <Typography.Text strong style={{ fontSize: 16, color: '#2E7D32' }}>
          AgroDoc Systems
        </Typography.Text>
      </Space>

      <div>
        {isAuthenticated && user ? (
          <Dropdown menu={{ items: userMenuItems }} placement="bottomRight">
            <Button type="text" style={{ height: 'auto', padding: '4px 8px' }}>
              <Space>
                <Avatar
                  size="small"
                  style={{ backgroundColor: '#2E7D32', cursor: 'pointer' }}
                  icon={!initials ? <UserOutlined /> : undefined}
                >
                  {initials}
                </Avatar>
                <span style={{ fontSize: 14 }}>
                  {user.first_name || user.login}
                </span>
              </Space>
            </Button>
          </Dropdown>
        ) : (
          <Button type="primary" onClick={() => setLoginOpen(true)}>
            Войти
          </Button>
        )}
      </div>

      <LoginModal open={loginOpen} onClose={() => setLoginOpen(false)} />
    </div>
  )
}
