import { useEffect, useState } from 'react'
import { Button, Card, Form, Input, Modal, Popconfirm, Space, Switch, Table, Tag, Typography, message } from 'antd'
import { PlusOutlined, EditOutlined, DeleteOutlined } from '@ant-design/icons'
import { authApi } from '../../api/auth'
import type { User } from '../../types/auth'
import dayjs from 'dayjs'

export default function UsersPage() {
  const [users, setUsers] = useState<User[]>([])
  const [loading, setLoading] = useState(true)
  const [open, setOpen] = useState(false)
  const [editing, setEditing] = useState<User | null>(null)
  const [saving, setSaving] = useState(false)
  const [form] = Form.useForm()

  const load = () => {
    setLoading(true)
    authApi.getUsers().then(({ data }) => setUsers(data)).finally(() => setLoading(false))
  }

  useEffect(() => { load() }, [])

  const openNew = () => { setEditing(null); form.resetFields(); setOpen(true) }
  const openEdit = (u: User) => { setEditing(u); form.setFieldsValue(u); setOpen(true) }

  const onSave = async () => {
    const values = await form.validateFields()
    setSaving(true)
    try {
      if (editing) {
        await authApi.updateUser(editing.id, values)
      } else {
        await authApi.createUser(values)
      }
      message.success('Сохранено')
      setOpen(false)
      load()
    } catch (e: any) {
      message.error(e.response?.data?.detail || 'Ошибка сохранения')
    } finally {
      setSaving(false)
    }
  }

  const onDelete = async (id: number) => {
    try {
      await authApi.deleteUser(id)
      message.success('Пользователь удалён')
      load()
    } catch {
      message.error('Ошибка удаления')
    }
  }

  const columns = [
    { title: 'Логин', dataIndex: 'username', key: 'username' },
    { title: 'Имя', key: 'name', render: (_: unknown, u: User) => `${u.first_name} ${u.last_name}`.trim() || '—' },
    { title: 'Email', dataIndex: 'email', key: 'email' },
    {
      title: 'Роль', key: 'role', width: 120,
      render: (_: unknown, u: User) => u.is_superuser
        ? <Tag color="red">Суперадмин</Tag>
        : u.is_staff ? <Tag color="blue">Администратор</Tag>
        : <Tag>Пользователь</Tag>,
    },
    {
      title: 'Зарегистрирован', dataIndex: 'date_joined', key: 'joined', width: 140,
      render: (v: string) => dayjs(v).format('DD.MM.YYYY'),
    },
    {
      title: '', key: 'actions', width: 90,
      render: (_: unknown, u: User) => (
        <Space>
          <Button size="small" icon={<EditOutlined />} onClick={() => openEdit(u)} />
          <Popconfirm title="Удалить пользователя?" onConfirm={() => onDelete(u.id)} okText="Да" cancelText="Нет">
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
        <Table dataSource={users} columns={columns} rowKey="id" loading={loading} size="small" />
      </Card>

      <Modal title={editing ? 'Редактировать пользователя' : 'Новый пользователь'}
        open={open} onCancel={() => setOpen(false)} onOk={onSave}
        okText="Сохранить" cancelText="Отмена" confirmLoading={saving} destroyOnClose>
        <Form form={form} layout="vertical" style={{ marginTop: 16 }}>
          <Form.Item label="Логин" name="username" rules={[{ required: true }]}><Input /></Form.Item>
          {!editing && (
            <Form.Item label="Пароль" name="password" rules={[{ required: true }]}><Input.Password /></Form.Item>
          )}
          <Form.Item label="Имя" name="first_name"><Input /></Form.Item>
          <Form.Item label="Фамилия" name="last_name"><Input /></Form.Item>
          <Form.Item label="Email" name="email"><Input type="email" /></Form.Item>
          <Form.Item label="Администратор" name="is_staff" valuePropName="checked"><Switch /></Form.Item>
        </Form>
      </Modal>
    </>
  )
}
