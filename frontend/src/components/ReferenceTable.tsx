import { useEffect, useState } from 'react'
import { Button, Card, Form, Modal, Popconfirm, Space, Switch, Table, message } from 'antd'
import { PlusOutlined, EditOutlined, DeleteOutlined } from '@ant-design/icons'
import type { ColumnsType } from 'antd/es/table'

interface Props<T extends { id: string }> {
  title: string
  api: {
    list: () => Promise<{ data: T[] }>
    create: (d: Partial<T>) => Promise<{ data: T }>
    update: (id: string, d: Partial<T>) => Promise<{ data: T }>
    remove: (id: string) => Promise<unknown>
  }
  columns: ColumnsType<T>
  formFields: React.ReactNode
}

export default function ReferenceTable<T extends { id: string }>({ title, api, columns, formFields }: Props<T>) {
  const [data, setData] = useState<T[]>([])
  const [loading, setLoading] = useState(true)
  const [open, setOpen] = useState(false)
  const [editing, setEditing] = useState<T | null>(null)
  const [saving, setSaving] = useState(false)
  const [form] = Form.useForm()

  const load = () => {
    setLoading(true)
    api.list().then(({ data: d }) => setData(d)).finally(() => setLoading(false))
  }

  useEffect(() => { load() }, [])

  const openNew = () => { setEditing(null); form.resetFields(); setOpen(true) }
  const openEdit = (row: T) => { setEditing(row); form.setFieldsValue(row); setOpen(true) }

  const onSave = async () => {
    const values = await form.validateFields()
    setSaving(true)
    try {
      if (editing) {
        await api.update(editing.id, values)
      } else {
        await api.create(values)
      }
      message.success('Сохранено')
      setOpen(false)
      load()
    } catch {
      message.error('Ошибка сохранения')
    } finally {
      setSaving(false)
    }
  }

  const onDelete = async (id: string) => {
    try {
      await api.remove(id)
      message.success('Удалено')
      load()
    } catch {
      message.error('Ошибка удаления')
    }
  }

  const actionCol: ColumnsType<T>[0] = {
    title: '',
    key: 'actions',
    width: 90,
    render: (_: unknown, row: T) => (
      <Space>
        <Button size="small" icon={<EditOutlined />} onClick={() => openEdit(row)} />
        <Popconfirm title="Удалить запись?" onConfirm={() => onDelete(row.id)} okText="Да" cancelText="Нет">
          <Button size="small" danger icon={<DeleteOutlined />} />
        </Popconfirm>
      </Space>
    ),
  }

  return (
    <>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 16 }}>
        <span style={{ fontSize: 20, fontWeight: 600 }}>{title}</span>
        <Button type="primary" icon={<PlusOutlined />} onClick={openNew}>Добавить</Button>
      </div>

      <Card>
        <Table dataSource={data} columns={[...columns, actionCol]} rowKey="id" loading={loading} size="small" />
      </Card>

      <Modal
        title={editing ? 'Редактировать' : 'Добавить'}
        open={open}
        onCancel={() => setOpen(false)}
        onOk={onSave}
        okText="Сохранить"
        cancelText="Отмена"
        confirmLoading={saving}
        destroyOnClose
      >
        <Form form={form} layout="vertical" style={{ marginTop: 16 }}>
          {formFields}
        </Form>
      </Modal>
    </>
  )
}
