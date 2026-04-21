import { useEffect, useState } from 'react'
import { Button, Card, Checkbox, Form, Input, Modal, Popconfirm, Select, Space, Switch, Table, Tag, Typography, message } from 'antd'
import { PlusOutlined, EditOutlined, DeleteOutlined, KeyOutlined } from '@ant-design/icons'
import { authApi } from '../../api/auth'
import { counterpartiesApi } from '../../api/reference'
import type { User } from '../../types/auth'
import type { Counterparty } from '../../types/reference'

const ROLE_OPTIONS = [
  { value: 'user',    label: 'Пользователь' },
  { value: 'manager', label: 'Менеджер' },
  { value: 'admin',   label: 'Администратор' },
]

const SECTION_OPTIONS = [
  { label: 'Дашборд',              value: 'dashboard' },
  { label: 'Справочники',          value: 'reference' },
  { label: 'Реестр сертификатов',  value: 'certificate_registry' },
  { label: 'Экспорт',              value: 'export' },
]

const ROLE_COLOR: Record<string, string> = {
  admin: 'red', manager: 'blue', user: 'default',
}

export default function UsersPage() {
  const [users, setUsers] = useState<User[]>([])
  const [loading, setLoading] = useState(true)
  const [open, setOpen] = useState(false)
  const [editing, setEditing] = useState<User | null>(null)
  const [saving, setSaving] = useState(false)
  const [form] = Form.useForm()

  const [resetOpen, setResetOpen] = useState(false)
  const [resetTarget, setResetTarget] = useState<User | null>(null)
  const [resetSaving, setResetSaving] = useState(false)
  const [resetForm] = Form.useForm()

  const [counterpartyOptions, setCounterpartyOptions] = useState<{ value: string; label: string }[]>([])
  const [counterpartySearch, setCounterpartySearch] = useState('')

  const load = () => {
    setLoading(true)
    authApi.getUsers().then(({ data }) => setUsers(data)).finally(() => setLoading(false))
  }

  useEffect(() => { load() }, [])

  useEffect(() => {
    if (!open) return
    counterpartiesApi
      .list({ active_only: 'true', ...(counterpartySearch ? { search: counterpartySearch } : {}) })
      .then(({ data }) =>
        setCounterpartyOptions(data.map((c: Counterparty) => ({ value: c.uuid, label: c.name_ru })))
      )
  }, [open, counterpartySearch])

  const openNew = () => {
    setEditing(null)
    form.resetFields()
    setCounterpartySearch('')
    setOpen(true)
  }

  const openEdit = (u: User) => {
    setEditing(u)
    form.setFieldsValue({
      login: u.login,
      last_name: u.last_name,
      first_name: u.first_name,
      middle_name: u.middle_name,
      email: u.email,
      phone: u.phone,
      job_title: u.job_title,
      role_code: u.role_code,
      counterparty: u.counterparty?.uuid ?? null,
      permissions: u.permissions || [],
      is_active: u.is_active,
    })
    setCounterpartySearch('')
    setOpen(true)
  }

  const onSave = async () => {
    const values = await form.validateFields()
    setSaving(true)
    try {
      if (editing) {
        const { password, ...rest } = values
        await authApi.updateUser(editing.uuid, password ? values : rest)
      } else {
        await authApi.createUser(values)
      }
      message.success('Сохранено')
      setOpen(false)
      load()
    } catch (e: any) {
      const err = e.response?.data
      if (err?.login) {
        form.setFields([{ name: 'login', errors: err.login }])
      } else if (err?.counterparty) {
        form.setFields([{ name: 'counterparty', errors: err.counterparty }])
      } else {
        message.error(err?.detail || 'Ошибка сохранения')
      }
    } finally {
      setSaving(false)
    }
  }

  const openReset = (u: User) => { setResetTarget(u); resetForm.resetFields(); setResetOpen(true) }

  const onResetPassword = async () => {
    const values = await resetForm.validateFields()
    if (!resetTarget) return
    setResetSaving(true)
    try {
      await authApi.updateUser(resetTarget.uuid, { password: values.password })
      message.success(`Пароль для «${resetTarget.login}» изменён`)
      setResetOpen(false)
    } catch (e: any) {
      message.error(e.response?.data?.detail || 'Ошибка смены пароля')
    } finally {
      setResetSaving(false)
    }
  }

  const onDelete = async (uuid: string) => {
    try {
      await authApi.deleteUser(uuid)
      message.success('Пользователь удалён')
      load()
    } catch {
      message.error('Ошибка удаления')
    }
  }

  const columns = [
    { title: 'Логин', dataIndex: 'login', key: 'login' },
    {
      title: 'ФИО', key: 'name',
      render: (_: unknown, u: User) =>
        [u.last_name, u.first_name, u.middle_name].filter(Boolean).join(' ') || '—',
    },
    {
      title: 'Организация', key: 'counterparty',
      render: (_: unknown, u: User) => u.counterparty?.name_ru || '—',
      ellipsis: true,
    },
    { title: 'Должность', dataIndex: 'job_title', key: 'job_title', render: (v: string | null) => v || '—' },
    { title: 'Email', dataIndex: 'email', key: 'email', render: (v: string | null) => v || '—' },
    { title: 'Телефон', dataIndex: 'phone', key: 'phone', render: (v: string | null) => v || '—' },
    {
      title: 'Роль', key: 'role', width: 140,
      render: (_: unknown, u: User) => {
        const opt = ROLE_OPTIONS.find(o => o.value === u.role_code)
        return <Tag color={ROLE_COLOR[u.role_code] || 'default'}>{opt?.label ?? u.role_code}</Tag>
      },
    },
    {
      title: 'Активен', key: 'active', width: 90,
      render: (_: unknown, u: User) => <Tag color={u.is_active ? 'green' : 'default'}>{u.is_active ? 'Да' : 'Нет'}</Tag>,
    },
    {
      title: '', key: 'actions', width: 100,
      render: (_: unknown, u: User) => (
        <Space>
          <Button size="small" icon={<EditOutlined />} onClick={() => openEdit(u)} />
          <Button size="small" icon={<KeyOutlined />} title="Сбросить пароль" onClick={() => openReset(u)} />
          <Popconfirm title="Удалить пользователя?" onConfirm={() => onDelete(u.uuid)} okText="Да" cancelText="Нет">
            <Button size="small" danger icon={<DeleteOutlined />} />
          </Popconfirm>
        </Space>
      ),
    },
  ]

  return (
    <>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 16 }}>
        <Typography.Title level={4} style={{ margin: 0 }}>Пользователи</Typography.Title>
        <Button type="primary" icon={<PlusOutlined />} onClick={openNew}>Добавить</Button>
      </div>
      <Card>
        <Table dataSource={users} columns={columns} rowKey="uuid" loading={loading} size="small" />
      </Card>

      <Modal
        title={editing ? 'Редактировать пользователя' : 'Новый пользователь'}
        open={open} onCancel={() => setOpen(false)} onOk={onSave}
        okText="Сохранить" cancelText="Отмена" confirmLoading={saving} destroyOnClose
        width={540}
      >
        <Form form={form} layout="vertical" style={{ marginTop: 16 }}>
          <Form.Item label="Логин" name="login" rules={[{ required: true, message: 'Обязательно' }]}>
            <Input disabled={!!editing} />
          </Form.Item>

          {!editing && (
            <Form.Item label="Пароль" name="password">
              <Input.Password placeholder="Оставьте пустым — пользователь задаст сам" />
            </Form.Item>
          )}

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
            <Form.Item label="Фамилия" name="last_name" rules={[{ required: true, message: 'Обязательно' }]} style={{ flex: 1 }}>
              <Input />
            </Form.Item>
            <Form.Item label="Имя" name="first_name" rules={[{ required: true, message: 'Обязательно' }]} style={{ flex: 1 }}>
              <Input />
            </Form.Item>
          </div>
          <Form.Item label="Отчество" name="middle_name">
            <Input />
          </Form.Item>
          <Form.Item label="Должность" name="job_title" rules={[{ required: true, message: 'Обязательно' }]}>
            <Input />
          </Form.Item>
          <div style={{ display: 'flex', gap: 8 }}>
            <Form.Item label="Телефон" name="phone" rules={[{ required: true, message: 'Обязательно' }]} style={{ flex: 1 }}>
              <Input placeholder="+7 (xxx) xxx-xx-xx" />
            </Form.Item>
            <Form.Item
              label="Email"
              name="email"
              rules={[{ required: true, message: 'Обязательно' }, { type: 'email', message: 'Некорректный email' }]}
              style={{ flex: 1 }}
            >
              <Input type="email" />
            </Form.Item>
          </div>
          <Form.Item label="Роль" name="role_code" rules={[{ required: true }]} initialValue="user">
            <Select options={ROLE_OPTIONS} />
          </Form.Item>
          <Form.Item label="Доступ к разделам" name="permissions" initialValue={[]}>
            <Checkbox.Group options={SECTION_OPTIONS} style={{ display: 'flex', flexWrap: 'wrap', gap: 8 }} />
          </Form.Item>
          {editing && (
            <Form.Item label="Активен" name="is_active" valuePropName="checked">
              <Switch />
            </Form.Item>
          )}
        </Form>
      </Modal>

      <Modal
        title={`Сброс пароля — ${resetTarget?.login}`}
        open={resetOpen} onCancel={() => setResetOpen(false)} onOk={onResetPassword}
        okText="Сохранить" cancelText="Отмена" confirmLoading={resetSaving} destroyOnClose
      >
        <Form form={resetForm} layout="vertical" style={{ marginTop: 16 }}>
          <Form.Item
            label="Новый пароль"
            name="password"
            rules={[{ required: true, min: 6, message: 'Минимум 6 символов' }]}
          >
            <Input.Password placeholder="Минимум 6 символов" />
          </Form.Item>
          <Form.Item
            label="Повторите пароль"
            name="password_confirm"
            dependencies={['password']}
            rules={[
              { required: true, message: 'Повторите пароль' },
              ({ getFieldValue }) => ({
                validator(_, value) {
                  if (!value || getFieldValue('password') === value) return Promise.resolve()
                  return Promise.reject(new Error('Пароли не совпадают'))
                },
              }),
            ]}
          >
            <Input.Password placeholder="Повторите пароль" />
          </Form.Item>
        </Form>
      </Modal>
    </>
  )
}
