import { useEffect, useState } from 'react'
import { Card, Col, Row, Statistic, Table, Tag, Typography, Button } from 'antd'
import { FileTextOutlined, CheckCircleOutlined, EditOutlined, InboxOutlined } from '@ant-design/icons'
import { useNavigate } from 'react-router-dom'
import { applicationsApi } from '../../api/applications'
import type { Application } from '../../types/application'
import dayjs from 'dayjs'

const STATUS_MAP: Record<string, { label: string; color: string }> = {
  draft: { label: 'Черновик', color: 'default' },
  completed: { label: 'Завершена', color: 'success' },
  archived: { label: 'Архив', color: 'orange' },
}

export default function DashboardPage() {
  const navigate = useNavigate()
  const [apps, setApps] = useState<Application[]>([])
  const [loading, setLoading] = useState(true)
  const [total, setTotal] = useState(0)

  useEffect(() => {
    applicationsApi.list().then(({ data }) => {
      setApps(data.results)
      setTotal(data.count)
    }).finally(() => setLoading(false))
  }, [])

  const drafts = apps.filter((a) => a.status === 'draft').length
  const completed = apps.filter((a) => a.status === 'completed').length
  const archived = apps.filter((a) => a.status === 'archived').length

  const columns = [
    { title: '№ заявки', dataIndex: 'application_number', key: 'num',
      render: (v: string, r: Application) => <Button type="link" onClick={() => navigate(`/applications/${r.id}`)}>{v}</Button> },
    { title: 'Продукт', dataIndex: 'product_rus', key: 'product', ellipsis: true },
    { title: 'Импортёр', dataIndex: 'importer_name_eng', key: 'importer', ellipsis: true },
    { title: 'Статус', dataIndex: 'status', key: 'status',
      render: (v: string) => <Tag color={STATUS_MAP[v]?.color}>{STATUS_MAP[v]?.label}</Tag> },
    { title: 'Создана', dataIndex: 'created_at', key: 'date',
      render: (v: string) => dayjs(v).format('DD.MM.YYYY') },
  ]

  return (
    <>
      <Typography.Title level={4} style={{ marginBottom: 24 }}>Главная</Typography.Title>

      <Row gutter={[16, 16]} style={{ marginBottom: 24 }}>
        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic title="Всего заявок" value={total} prefix={<FileTextOutlined style={{ color: '#1a3c6e' }} />} />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic title="Черновики" value={drafts} prefix={<EditOutlined style={{ color: '#8c8c8c' }} />} />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic title="Завершены" value={completed} prefix={<CheckCircleOutlined style={{ color: '#2e7d32' }} />} valueStyle={{ color: '#2e7d32' }} />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic title="Архив" value={archived} prefix={<InboxOutlined style={{ color: '#fa8c16' }} />} valueStyle={{ color: '#fa8c16' }} />
          </Card>
        </Col>
      </Row>

      <Card
        title="Последние заявки"
        extra={<Button type="primary" onClick={() => navigate('/applications')}>Все заявки</Button>}
      >
        <Table
          dataSource={apps.slice(0, 10)}
          columns={columns}
          rowKey="id"
          loading={loading}
          pagination={false}
          size="small"
        />
      </Card>
    </>
  )
}
