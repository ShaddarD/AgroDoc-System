import { useEffect, useState } from 'react'
import { Button, Card, Input, Select, Space, Table, Tag, Typography } from 'antd'
import { PlusOutlined, SearchOutlined } from '@ant-design/icons'
import { useNavigate } from 'react-router-dom'
import { applicationsApi } from '../../api/applications'
import type { Application } from '../../types/application'

type ApplicationStatus = 'draft' | 'completed' | 'archived'
import dayjs from 'dayjs'

const STATUS_MAP: Record<ApplicationStatus, { label: string; color: string }> = {
  draft: { label: 'Черновик', color: 'default' },
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

  const columns = [
    {
      title: '№ заявки', dataIndex: 'application_number', key: 'num',
      render: (v: string, r: Application) => (
        <Button type="link" style={{ padding: 0 }} onClick={() => navigate(`/applications/${r.id}`)}>{v}</Button>
      ),
    },
    { title: 'Продукт', dataIndex: 'product_rus', key: 'product', ellipsis: true },
    { title: 'Импортёр', dataIndex: 'importer_name_eng', key: 'importer', ellipsis: true },
    {
      title: 'Статус', dataIndex: 'status', key: 'status', width: 120,
      render: (v: ApplicationStatus) => <Tag color={STATUS_MAP[v]?.color}>{STATUS_MAP[v]?.label}</Tag>,
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
        <Button type="primary" icon={<PlusOutlined />} onClick={() => navigate('/applications/new')}>
          Новая заявка
        </Button>
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
            style={{ width: 160 }}
            value={status || undefined}
            onChange={(v) => setStatus(v || '')}
            allowClear
            options={[
              { label: 'Черновик', value: 'draft' },
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
          pagination={{
            total,
            current: page,
            pageSize: 20,
            onChange: (p) => { setPage(p); fetchApps(p) },
            showTotal: (t) => `Всего ${t} заявок`,
          }}
          onRow={(r) => ({ onDoubleClick: () => navigate(`/applications/${r.id}`) })}
        />
      </Card>
    </>
  )
}
