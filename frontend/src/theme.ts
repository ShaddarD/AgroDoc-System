import type { ThemeConfig } from 'antd'

const theme: ThemeConfig = {
  token: {
    colorPrimary: '#0E9749',
    colorSuccess: '#12b057',
    colorLink: '#0E9749',
    colorWarning: '#F4B400',
    borderRadius: 8,
    fontFamily: "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
    colorBgLayout: '#F9FAFB',
  },
  components: {
    Layout: {
      siderBg: '#0a6b35',
      triggerBg: '#0a6b35',
    },
    Menu: {
      darkItemBg: '#0a6b35',
      darkSubMenuItemBg: '#085528',
      darkItemSelectedBg: '#F4B400',
      darkItemSelectedColor: '#1F2937',
      darkItemHoverBg: '#0E9749',
    },
    Button: {
      colorPrimary: '#0E9749',
    },
  },
}

export default theme
