import { useState } from 'react'
import { Avatar, Button, Drawer, Dropdown, Grid, Layout, Space, Typography } from 'antd'
import { LogoutOutlined, MenuOutlined, UserOutlined, AppstoreOutlined } from '@ant-design/icons'
import { useNavigate } from 'react-router-dom'
import { useAuthStore } from '../../store/authStore'
import { authApi } from '../../api/auth'
import Sidebar from './Sidebar'
import AlanDosmotraPage from '../../pages/AlanDosmotra/AlanDosmotraPage'

const { Header, Content } = Layout
const { useBreakpoint } = Grid

export default function PublicPlanLayout() {
  const navigate = useNavigate()
  const { user, isAuthenticated, refreshToken, clearAuth } = useAuthStore()
  const [drawerOpen, setDrawerOpen] = useState(false)
  const screens = useBreakpoint()
  const isMobile = !screens.md

  const handleLogout = async () => {
    try {
      if (refreshToken) await authApi.logout(refreshToken)
    } catch { /* ignore */ }
    clearAuth()
  }

  const userMenuItems = [
    {
      key: 'username',
      label: <Typography.Text type="secondary">{user?.login}</Typography.Text>,
      disabled: true,
    },
    { type: 'divider' as const },
    { key: 'system', icon: <AppstoreOutlined />, label: 'Войти в систему', onClick: () => navigate('/dashboard') },
    { key: 'logout', icon: <LogoutOutlined />, label: 'Выйти', danger: true, onClick: handleLogout },
  ]

  return (
    <Layout style={{ minHeight: '100vh' }}>
      {/* Боковое меню — только для авторизованных */}
      {isAuthenticated && (
        <Drawer
          placement="left"
          open={drawerOpen}
          onClose={() => setDrawerOpen(false)}
          width={220}
          styles={{ body: { padding: 0, background: '#001529' }, header: { display: 'none' } }}
        >
          <div style={{ padding: '16px', textAlign: 'center', borderBottom: '1px solid rgba(255,255,255,0.1)' }}>
            <img src="/logo-primary.png" alt="AgroDoc" style={{ height: 48, objectFit: 'contain' }} />
          </div>
          <Sidebar onNavigate={() => setDrawerOpen(false)} />
        </Drawer>
      )}

      <Header style={{
        background: '#fff',
        padding: '0 16px',
        boxShadow: '0 1px 4px rgba(0,0,0,0.1)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        position: 'sticky',
        top: 0,
        zIndex: 99,
      }}>
        <Space>
          {/* Бургер — только для авторизованных */}
          {isAuthenticated && (
            <Button type="text" icon={<MenuOutlined />} onClick={() => setDrawerOpen(true)} />
          )}
          <Typography.Text strong style={{ fontSize: isMobile ? 13 : 16, color: '#1a3c6e' }}>
            {isMobile ? 'АгроДок' : 'AgroDoc Systems'} — План досмотра
          </Typography.Text>
        </Space>

        {isAuthenticated ? (
          /* Авторизован: аватар с дропдауном */
          <Dropdown menu={{ items: userMenuItems }} placement="bottomRight">
            <Button type="text" style={{ height: 'auto', padding: '4px 8px' }}>
              <Space>
                <Avatar size="small" icon={<UserOutlined />} style={{ backgroundColor: '#1a3c6e' }} />
                {!isMobile && <span>{user?.first_name || user?.login}</span>}
              </Space>
            </Button>
          </Dropdown>
        ) : (
          /* Не авторизован: кнопка входа */
          <Button type="primary" onClick={() => navigate('/login')}>
            Войти
          </Button>
        )}
      </Header>

      <Content style={{ padding: isMobile ? '12px 8px' : '16px 24px' }}>
        <AlanDosmotraPage />
      </Content>
    </Layout>
  )
}
