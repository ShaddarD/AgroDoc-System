import type { ThemeConfig } from 'antd'

const theme: ThemeConfig = {
  token: {
    colorPrimary: '#1a3c6e',
    colorSuccess: '#2e7d32',
    colorLink: '#1a3c6e',
    borderRadius: 6,
    fontFamily: "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
    colorBgLayout: '#f0f2f5',
  },
  components: {
    Layout: {
      siderBg: '#1a3c6e',
      triggerBg: '#152f58',
    },
    Menu: {
      darkItemBg: '#1a3c6e',
      darkSubMenuItemBg: '#152f58',
      darkItemSelectedBg: '#2e7d32',
      darkItemHoverBg: '#234d8a',
    },
    Button: {
      colorPrimary: '#1a3c6e',
    },
  },
}

export default theme
