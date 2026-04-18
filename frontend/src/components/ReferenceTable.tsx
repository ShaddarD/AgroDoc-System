import { useEffect, useState } from 'react'
import { Button, Card, Form, Modal, Popconfirm, Space, Table, Tag, message } from 'antd'
import { PlusOutlined, EditOutlined, DeleteOutlined, LockOutlined } from '@ant-design/icons'
import type { ColumnsType } from 'antd/es/table'

interface Props<T extends { uuid: string }> {
  title: string
  api: {
    list: (params?: Record<string, string>) => Promise<{ data: T[] }>
    create: (d: Partial<T>) => Promise<{ data: T }>
    update: (uuid: string, d: Partial<T>) => Promise<{ data: T }>
    remove: (uuid: string) => Promise<unknown>
  }
  columns: ColumnsType<T>
  formFields: React.ReactNode
  canEdit?: boolean
  canAdd?: boolean
  listParams?: Record<string, string>
  modalWidth?: number
  onBeforeOpen?: (row: T | null, form: ReturnType<typeof Form.useForm>[0]) => void
}

export default function ReferenceTable<T extends { uuid: string }>({
  title, api, columns, formFields, canEdit = false, canAdd = false,
  listParams, modalWidth = 520, onBeforeOpen,
}: Props<T>) {
  const [data, setData] = useState<T[]>([])
  const [loading, setLoading] = useState(true)
  const [open, setOpen] = useState(false)
  const [editing, setEditing] = useState<T | null>(null)
  const [saving, setSaving] = useState(false)
  const [form] = Form.useForm()

  const load = () => {
    setLoading(true)
    api.list(listParams).then(({ data: d }) => setData(d)).finally(() => setLoading(false))
  }

  useEffect(() => { load() }, [])

  const openNew = () => {
    setEditing(null)
    form.resetFields()
    onBeforeOpen?.(null, form)
    setOpen(true)
  }
  const openEdit = (row: T) => {
    setEditing(row)
    form.setFieldsValue(row)
    onBeforeOpen?.(row, form)
    setOpen(true)
  }

  const onSave = async () => {
    const values = await form.validateFields()
    setSaving(true)
    try {
      if (editing) {
        await api.update(editing.uuid, values)
      } else {
        await api.create(values)
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

  const onDelete = async (uuid: string) => {
    try {
      await api.remove(uuid)
      message.success('Удалено')
      load()
    } catch (e: any) {
      message.error(e.response?.data?.detail || 'Ошибка удаления')
    }
  }

  const actionCol: ColumnsType<T>[0] = {
    title: '',
    key: 'actions',
    width: canEdit ? 90 : 0,
    render: (_: unknown, row: T) => canEdit ? (
      <Space>
        <Button size="small" icon={<EditOutlined />} onClick={() => openEdit(row)} />
        <Popconfirm title="Удалить запись?" onConfirm={() => onDelete(row.uuid)} okText="Да" cancelText="Нет">
          <Button size="small" danger icon={<DeleteOutlined />} />
        </Popconfirm>
      </Space>
    ) : null,
  }

  return (
    <>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
        <span style={{ fontSize: 20, fontWeight: 600 }}>{title}</span>
        {canAdd ? (
          <Button type="primary" icon={<PlusOutlined />} onClick={openNew}>Добавить</Button>
        ) : (
          <Tag icon={<LockOutlined />} color="default">Только просмотр</Tag>
        )}
      </div>

      <Card>
        <Table
          dataSource={data}
          columns={[...columns, ...(canEdit ? [actionCol] : [])]}
          rowKey="uuid"
          loading={loading}
          size="small"
        />
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
        width={modalWidth}
      >
        <Form form={form} layout="vertical" style={{ marginTop: 16 }}>
          {formFields}
        </Form>
      </Modal>
    </>
  )
}
