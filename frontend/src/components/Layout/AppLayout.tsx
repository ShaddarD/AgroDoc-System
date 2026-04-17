import { useState, useEffect } from 'react'
import { Drawer, Grid, Layout } from 'antd'
import { Outlet } from 'react-router-dom'
import Sidebar from './Sidebar'
import AppHeader from './AppHeader'
import { useAuthStore } from '../../store/authStore'
import { authApi } from '../../api/auth'

const { Sider, Header, Content } = Layout
const { useBreakpoint } = Grid

export default function AppLayout() {
  const [collapsed, setCollapsed] = useState(false)
  const [drawerOpen, setDrawerOpen] = useState(false)
  const { setUser, user } = useAuthStore()
  const screens = useBreakpoint()
  const isMobile = !screens.md

  useEffect(() => {
    if (!user) {
      authApi.me().then((r) => setUser(r.data)).catch(() => {})
    }
  }, [])

  // Закрыть drawer при переходе на desktop
  useEffect(() => {
    if (!isMobile) setDrawerOpen(false)
  }, [isMobile])

  const logo = (small: boolean) => (
    <div style={{
      padding: small ? '16px 8px' : '16px',
      textAlign: 'center',
      borderBottom: '1px solid rgba(255,255,255,0.1)',
    }}>
      <img
        src="/logo-primary.png"
        alt="AgroDoc"
        style={{ height: small ? 32 : 48, transition: 'height 0.2s', objectFit: 'contain' }}
      />
    </div>
  )

  return (
    <Layout style={{ minHeight: '100vh' }}>
      {/* Десктоп: фиксированный Sider */}
      {!isMobile && (
        <Sider
          collapsible
          collapsed={collapsed}
          onCollapse={setCollapsed}
          width={220}
          style={{ position: 'fixed', height: '100vh', left: 0, top: 0, bottom: 0, zIndex: 100 }}
        >
          {logo(collapsed)}
          <Sidebar onNavigate={() => {}} />
        </Sider>
      )}

      {/* Мобайл: Drawer */}
      {isMobile && (
        <Drawer
          placement="left"
          open={drawerOpen}
          onClose={() => setDrawerOpen(false)}
          width={220}
          styles={{ body: { padding: 0, background: '#001529' }, header: { display: 'none' } }}
        >
          {logo(false)}
          <Sidebar onNavigate={() => setDrawerOpen(false)} />
        </Drawer>
      )}

      <Layout style={{ marginLeft: isMobile ? 0 : (collapsed ? 80 : 220), transition: 'margin-left 0.2s' }}>
        <Header style={{ background: '#fff', padding: 0, boxShadow: '0 1px 4px rgba(0,0,0,0.1)', position: 'sticky', top: 0, zIndex: 99 }}>
          <AppHeader onMenuToggle={isMobile ? () => setDrawerOpen(true) : undefined} />
        </Header>
        <Content style={{ margin: '16px 12px', minHeight: 280 }}>
          <Outlet />
        </Content>
      </Layout>
    </Layout>
  )
}
