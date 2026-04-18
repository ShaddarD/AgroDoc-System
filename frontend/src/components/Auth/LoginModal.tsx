import { useEffect, useState } from 'react'
import { Alert, Button, Form, Input, Modal, Select, Tabs, Typography, message } from 'antd'
import { LockOutlined, UserOutlined } from '@ant-design/icons'
import { authApi } from '../../api/auth'
import { counterpartiesApi } from '../../api/reference'
import { useAuthStore } from '../../store/authStore'
import type { Counterparty } from '../../types/reference'

interface Props {
  open: boolean
  onClose: () => void
}

type LoginStep = 'login' | 'set_password'

export default function LoginModal({ open, onClose }: Props) {
  const { setAuth } = useAuthStore()
  const [loginForm] = Form.useForm()
  const [registerForm] = Form.useForm()
  const [setPasswordForm] = Form.useForm()

  const [step, setStep] = useState<LoginStep>('login')
  const [accountUuid, setAccountUuid] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [activeTab, setActiveTab] = useState<'login' | 'register'>('login')

  const [counterpartyOptions, setCounterpartyOptions] = useState<{ value: string; label: string }[]>([])
  const [counterpartySearch, setCounterpartySearch] = useState('')

  useEffect(() => {
    if (activeTab !== 'register') return
    counterpartiesApi
      .list({ active_only: 'true', ...(counterpartySearch ? { search: counterpartySearch } : {}) })
      .then(({ data }) =>
        setCounterpartyOptions(data.map((c: Counterparty) => ({ value: c.uuid, label: c.name_ru })))
      )
  }, [activeTab, counterpartySearch])

  const reset = () => {
    setStep('login')
    setAccountUuid(null)
    setError(null)
    loginForm.resetFields()
    registerForm.resetFields()
    setPasswordForm.resetFields()
    setActiveTab('login')
    setCounterpartySearch('')
  }

  const handleClose = () => {
    reset()
    onClose()
  }

  const handleLogin = async () => {
    const values = await loginForm.validateFields()
    setLoading(true)
    setError(null)
    try {
      const { data } = await authApi.login(values.login, values.password)
      if ('needs_password_setup' in data && data.needs_password_setup) {
        setAccountUuid(data.account_uuid)
        setStep('set_password')
        return
      }
      if ('access' in data) {
        setAuth(data.user, data.access, data.refresh)
        message.success(`Добро пожаловать, ${data.user.first_name}!`)
        handleClose()
      }
    } catch (e: any) {
      setError(e.response?.data?.message || 'Неверный логин или пароль')
    } finally {
      setLoading(false)
    }
  }

  const handleSetPassword = async () => {
    const values = await setPasswordForm.validateFields()
    if (values.password !== values.password_confirm) {
      setPasswordForm.setFields([{ name: 'password_confirm', errors: ['Пароли не совпадают'] }])
      return
    }
    setLoading(true)
    setError(null)
    try {
      const { data } = await authApi.setPassword(accountUuid!, values.password)
      setAuth(data.user, data.access, data.refresh)
      message.success('Пароль установлен. Добро пожаловать!')
      handleClose()
    } catch (e: any) {
      setError(e.response?.data?.detail || 'Ошибка установки пароля')
    } finally {
      setLoading(false)
    }
  }

  const handleRegister = async () => {
    const values = await registerForm.validateFields()
    if (values.password !== values.password_confirm) {
      registerForm.setFields([{ name: 'password_confirm', errors: ['Пароли не совпадают'] }])
      return
    }
    setLoading(true)
    setError(null)
    try {
      const { data } = await authApi.register(values)
      setAuth(data.user, data.access, data.refresh)
      message.success('Аккаунт создан. Добро пожаловать!')
      handleClose()
    } catch (e: any) {
      const errs = e.response?.data
      if (errs?.login) {
        registerForm.setFields([{ name: 'login', errors: errs.login }])
      } else if (errs?.counterparty) {
        registerForm.setFields([{ name: 'counterparty', errors: errs.counterparty }])
      } else {
        setError(errs?.detail || 'Ошибка регистрации')
      }
    } finally {
      setLoading(false)
    }
  }

  const modalTitle = step === 'set_password' ? 'Создайте пароль для входа' : 'AgroDoc Systems'

  return (
    <Modal
      open={open}
      onCancel={handleClose}
      footer={null}
      width={460}
      centered
      title={
        <div style={{ textAlign: 'center', paddingTop: 8 }}>
          <img src="/logo-primary.png" alt="AgroDoc" style={{ height: 40, marginBottom: 4 }} />
          <Typography.Title level={5} style={{ margin: 0, color: '#1F2937' }}>
            {modalTitle}
          </Typography.Title>
        </div>
      }
      destroyOnClose
      afterClose={reset}
    >
      {error && (
        <Alert message={error} type="error" showIcon style={{ marginBottom: 16 }} />
      )}

      {step === 'set_password' && (
        <Form form={setPasswordForm} layout="vertical">
          <Typography.Text type="secondary" style={{ display: 'block', marginBottom: 16 }}>
            Для этого аккаунта ещё не задан пароль. Придумайте пароль для входа.
          </Typography.Text>
          <Form.Item name="password" label="Новый пароль" rules={[{ required: true, min: 6, message: 'Минимум 6 символов' }]}>
            <Input.Password prefix={<LockOutlined />} placeholder="Минимум 6 символов" />
          </Form.Item>
          <Form.Item name="password_confirm" label="Повторите пароль" rules={[{ required: true, message: 'Повторите пароль' }]}>
            <Input.Password prefix={<LockOutlined />} placeholder="Повторите пароль" />
          </Form.Item>
          <Button type="primary" block loading={loading} onClick={handleSetPassword} style={{ marginTop: 8 }}>
            Установить пароль
          </Button>
          <Button type="link" block onClick={() => setStep('login')} style={{ marginTop: 4 }}>
            ← Назад
          </Button>
        </Form>
      )}

      {step === 'login' && (
        <Tabs
          activeKey={activeTab}
          onChange={(k) => { setActiveTab(k as 'login' | 'register'); setError(null) }}
          centered
          items={[
            {
              key: 'login',
              label: 'Войти',
              children: (
                <Form form={loginForm} layout="vertical" onFinish={handleLogin}>
                  <Form.Item name="login" rules={[{ required: true, message: 'Введите логин' }]}>
                    <Input prefix={<UserOutlined />} placeholder="Логин" size="large" />
                  </Form.Item>
                  <Form.Item name="password" rules={[{ required: true, message: 'Введите пароль' }]}>
                    <Input.Password prefix={<LockOutlined />} placeholder="Пароль" size="large" />
                  </Form.Item>
                  <Button type="primary" htmlType="submit" block size="large" loading={loading}>
                    Войти
                  </Button>
                </Form>
              ),
            },
            {
              key: 'register',
              label: 'Регистрация',
              children: (
                <Form form={registerForm} layout="vertical" onFinish={handleRegister}>
                  <Form.Item name="login" label="Логин" rules={[{ required: true, message: 'Введите логин' }]}>
                    <Input prefix={<UserOutlined />} placeholder="Логин для входа" />
                  </Form.Item>

                  <Form.Item
                    name="counterparty"
                    label="Организация (контрагент)"
                    rules={[{ required: true, message: 'Выберите организацию' }]}
                  >
                    <Select
                      showSearch
                      placeholder="Начните вводить название..."
                      filterOption={false}
                      onSearch={setCounterpartySearch}
                      options={counterpartyOptions}
                      notFoundContent="Не найдено"
                    />
                  </Form.Item>

                  <div style={{ display: 'flex', gap: 8 }}>
                    <Form.Item name="last_name" label="Фамилия" rules={[{ required: true, message: 'Обязательно' }]} style={{ flex: 1 }}>
                      <Input />
                    </Form.Item>
                    <Form.Item name="first_name" label="Имя" rules={[{ required: true, message: 'Обязательно' }]} style={{ flex: 1 }}>
                      <Input />
                    </Form.Item>
                  </div>
                  <Form.Item name="middle_name" label="Отчество">
                    <Input />
                  </Form.Item>
                  <Form.Item name="job_title" label="Должность" rules={[{ required: true, message: 'Обязательно' }]}>
                    <Input />
                  </Form.Item>
                  <Form.Item name="phone" label="Телефон" rules={[{ required: true, message: 'Обязательно' }]}>
                    <Input placeholder="+7 (xxx) xxx-xx-xx" />
                  </Form.Item>
                  <Form.Item
                    name="email"
                    label="Email"
                    rules={[{ required: true, message: 'Обязательно' }, { type: 'email', message: 'Некорректный email' }]}
                  >
                    <Input type="email" />
                  </Form.Item>
                  <Form.Item name="password" label="Пароль" rules={[{ required: true, min: 6, message: 'Минимум 6 символов' }]}>
                    <Input.Password prefix={<LockOutlined />} />
                  </Form.Item>
                  <Form.Item name="password_confirm" label="Повторите пароль" rules={[{ required: true, message: 'Повторите пароль' }]}>
                    <Input.Password prefix={<LockOutlined />} />
                  </Form.Item>
                  <Button type="primary" htmlType="submit" block loading={loading}>
                    Создать аккаунт
                  </Button>
                </Form>
              ),
            },
          ]}
        />
      )}
    </Modal>
  )
}
