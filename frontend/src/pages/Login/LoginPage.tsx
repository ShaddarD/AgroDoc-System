import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Card, Form, Input, Button, Alert, Typography } from 'antd'
import { UserOutlined, LockOutlined } from '@ant-design/icons'
import { authApi } from '../../api/auth'
import { useAuthStore } from '../../store/authStore'

export default function LoginPage() {
  const navigate = useNavigate()
  const setAuth = useAuthStore((s) => s.setAuth)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const onFinish = async (values: { username: string; password: string }) => {
    setLoading(true)
    setError('')
    try {
      const { data } = await authApi.login(values.username, values.password)
      setAuth(data.user, data.access, data.refresh)
      navigate('/dashboard')
    } catch (e: any) {
      setError(e.response?.data?.message || 'Ошибка входа. Проверьте логин и пароль.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{
      minHeight: '100vh',
      background: 'linear-gradient(135deg, #1a3c6e 0%, #2e7d32 100%)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
    }}>
      <Card style={{ width: 380, borderRadius: 12, boxShadow: '0 8px 32px rgba(0,0,0,0.2)' }}>
        <div style={{ textAlign: 'center', marginBottom: 32 }}>
          <img src="/logo-primary.png" alt="AgroDoc" style={{ height: 72, marginBottom: 16 }} />
          <Typography.Title level={4} style={{ margin: 0, color: '#1a3c6e' }}>
            Вход в систему
          </Typography.Title>
          <Typography.Text type="secondary">AgroDoc Systems</Typography.Text>
        </div>

        {error && <Alert message={error} type="error" showIcon style={{ marginBottom: 16 }} />}

        <Form layout="vertical" onFinish={onFinish} autoComplete="off">
          <Form.Item name="username" rules={[{ required: true, message: 'Введите логин' }]}>
            <Input prefix={<UserOutlined />} placeholder="Логин" size="large" />
          </Form.Item>
          <Form.Item name="password" rules={[{ required: true, message: 'Введите пароль' }]}>
            <Input.Password prefix={<LockOutlined />} placeholder="Пароль" size="large" />
          </Form.Item>
          <Form.Item>
            <Button type="primary" htmlType="submit" block size="large" loading={loading}
              style={{ background: '#1a3c6e' }}>
              Войти
            </Button>
          </Form.Item>
        </Form>
      </Card>
    </div>
  )
}
