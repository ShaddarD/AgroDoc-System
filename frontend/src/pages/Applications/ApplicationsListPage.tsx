import { useEffect, useRef, useState } from 'react'
import { Button, Card, Dropdown, Input, message, Modal, Select, Space, Table, Tag, Typography } from 'antd'
import { CopyOutlined, DeleteOutlined, EditOutlined, PlusOutlined, SearchOutlined } from '@ant-design/icons'
import { useNavigate } from 'react-router-dom'
import { applicationsApi } from '../../api/applications'
import type { Application } from '../../types/application'
import dayjs from 'dayjs'

type ApplicationStatus = 'draft' | 'completed' | 'archived' | 'filled' | 'ready_to_print'

const STATUS_MAP: Record<string, { label: string; color: string }> = {
  draft: { label: 'Черновик', color: 'default' },
  filled: { label: 'Заполнено', color: 'blue' },
  ready_to_print: { label: 'Готово к печати', color: 'green' },
  completed: { label: 'Завершена', color: 'success' },
  archived: { label: 'Архив', color: 'orange' },
}

export default function ApplicationsListPage() {
  const navigate = useNavigate()
  const [apps, setApps] = useState<Application[]>([])
  const [loading, setLoading] = useState(true)
  const [total, setTotal] = useState(0)
  const [search, setSearch] = useState('')
  const [status, setStatus] = useState<string>('')
  const [page, setPage] = useState(1)
  const [selectedId, setSelectedId] = useState<string | null>(null)
  const contextMenuRecord = useRef<Application | null>(null)

  const fetchApps = (pg = page) => {
    setLoading(true)
    const params: Record<string, string> = { page: String(pg) }
    if (search) params.search = search
    if (status) params.status = status
    applicationsApi.list(params).then(({ data }) => {
      setApps(data.results)
      setTotal(data.count)
    }).finally(() => setLoading(false))
  }

  useEffect(() => { fetchApps(1) }, [search, status])

  const copyApplication = async (id: string) => {
    try {
      const { data } = await applicationsApi.get(id)
      const { id: _, application_number: __, created_at: ___, updated_at: ____, ...rest } = data as any
      const copy = { ...rest, status: 'draft', status_code: 'draft' }
      const { data: newApp } = await applicationsApi.create(copy)
      message.success('Заявка скопирована')
      navigate(`/applications/${newApp.id}/edit`)
    } catch {
      message.error('Ошибка копирования заявки')
    }
  }

  const deleteApplication = (id: string, num: string) => {
    Modal.confirm({
      title: `Удалить заявку № ${num}?`,
      content: 'Это действие нельзя отменить.',
      okText: 'Удалить',
      okType: 'danger',
      cancelText: 'Отмена',
      onOk: async () => {
        await applicationsApi.remove(id)
        message.success('Заявка удалена')
        fetchApps()
      },
    })
  }

  const contextMenuItems = (record: Application) => ({
    items: [
      {
        key: 'open',
        icon: <EditOutlined />,
        label: 'Открыть',
        onClick: () => navigate(`/applications/${record.id}/edit`),
      },
      {
        key: 'copy',
        icon: <CopyOutlined />,
        label: 'Копировать',
        onClick: () => copyApplication(record.id),
      },
      { type: 'divider' as const },
      {
        key: 'delete',
        icon: <DeleteOutlined />,
        label: 'Удалить',
        danger: true,
        onClick: () => deleteApplication(record.id, record.application_number),
      },
    ],
  })

  const ContextMenuRow = ({ children, ...props }: any) => {
    const record = contextMenuRecord.current
    if (!record) return <tr {...props}>{children}</tr>
    return (
      <Dropdown menu={contextMenuItems(record)} trigger={['contextMenu']}>
        <tr {...props}>{children}</tr>
      </Dropdown>
    )
  }

  const columns = [
    {
      title: '№ заявки', dataIndex: 'application_number', key: 'num',
      render: (v: string, r: Application) => (
        <Button type="link" style={{ padding: 0 }} onClick={() => navigate(`/applications/${r.id}`)}>{v}</Button>
      ),
    },
    { title: 'Продукт', dataIndex: 'product_rus', key: 'product', ellipsis: true },
    { title: 'Получатель', dataIndex: 'importer_name_eng', key: 'importer', ellipsis: true },
    {
      title: 'Статус', dataIndex: 'status', key: 'status', width: 140,
      render: (v: string) => {
        const s = STATUS_MAP[v] ?? { label: v, color: 'default' }
        return <Tag color={s.color}>{s.label}</Tag>
      },
    },
    {
      title: 'Создана', dataIndex: 'created_at', key: 'date', width: 110,
      render: (v: string) => dayjs(v).format('DD.MM.YYYY'),
    },
    {
      title: '', key: 'actions', width: 80,
      render: (_: unknown, r: Application) => (
        <Button size="small" onClick={() => navigate(`/applications/${r.id}/edit`)}>Открыть</Button>
      ),
    },
  ]

  return (
    <>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
        <Typography.Title level={4} style={{ margin: 0 }}>Заявки</Typography.Title>
        <Space>
          {selectedId && (
            <Button icon={<CopyOutlined />} onClick={() => copyApplication(selectedId)}>
              Копировать заявку
            </Button>
          )}
          <Button type="primary" icon={<PlusOutlined />} onClick={() => navigate('/applications/new')}>
            Новая заявка
          </Button>
        </Space>
      </div>

      <Card>
        <Space style={{ marginBottom: 16 }}>
          <Input
            placeholder="Поиск по номеру, продукту, контейнерам..."
            prefix={<SearchOutlined />}
            style={{ width: 320 }}
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            allowClear
          />
          <Select
            placeholder="Статус"
            style={{ width: 180 }}
            value={status || undefined}
            onChange={(v) => setStatus(v || '')}
            allowClear
            options={[
              { label: 'Черновик', value: 'draft' },
              { label: 'Заполнено', value: 'filled' },
              { label: 'Готово к печати', value: 'ready_to_print' },
              { label: 'Завершена', value: 'completed' },
              { label: 'Архив', value: 'archived' },
            ]}
          />
        </Space>

        <Table
          dataSource={apps}
          columns={columns}
          rowKey="id"
          loading={loading}
          rowClassName={(r) => r.id === selectedId ? 'ant-table-row-selected' : ''}
          components={{ body: { row: ContextMenuRow } }}
          onRow={(r) => ({
            onClick: () => setSelectedId((prev) => prev === r.id ? null : r.id),
            onDoubleClick: () => navigate(`/applications/${r.id}`),
            onMouseEnter: () => { contextMenuRecord.current = r },
          })}
          pagination={{
            total,
            current: page,
            pageSize: 20,
            onChange: (p) => { setPage(p); fetchApps(p) },
            showTotal: (t) => `Всего ${t} заявок`,
          }}
        />
      </Card>
    </>
  )
}
