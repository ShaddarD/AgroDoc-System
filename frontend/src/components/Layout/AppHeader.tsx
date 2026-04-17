import { Button, Space, Typography } from 'antd'
import { MenuOutlined } from '@ant-design/icons'

interface Props {
  onMenuToggle?: () => void
}

export default function AppHeader({ onMenuToggle }: Props) {
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
    </div>
  )
}
