import { useEffect, useState } from 'react'
import {
  Button, Card, DatePicker, Form, Input, InputNumber, Modal,
  Popconfirm, Select, Space, Table, Tag, Tooltip, Typography, message,
} from 'antd'
import type { ColumnsType } from 'antd/es/table'
import {
  PlusOutlined, EditOutlined, DeleteOutlined,
  SearchOutlined, ReloadOutlined, FilterOutlined,
} from '@ant-design/icons'
import dayjs from 'dayjs'
import { inspectionRecordsApi, type InspectionRecord } from '../../api/inspectionRecords'
import { useAuthStore } from '../../store/authStore'

const QUARANTINE_LABELS: Record<string, { label: string; color: string }> = {
  own: { label: 'Свои', color: 'blue' },
  client: { label: 'Клиентские', color: 'purple' },
  shared: { label: 'Совместные', color: 'cyan' },
  other: { label: 'Другое', color: 'default' },
}

const CARGO_STATUS_LABELS: Record<string, { label: string; color: string }> = {
  waiting: { label: 'Ожидает', color: 'default' },
  loaded: { label: 'Погружен', color: 'processing' },
  shipped: { label: 'Отгружен', color: 'blue' },
  on_way: { label: 'В пути', color: 'warning' },
  delivered: { label: 'Доставлен', color: 'success' },
}

const DOC_STATUS_LABELS: Record<string, { label: string; color: string }> = {
  not_ready: { label: 'Не готовы', color: 'error' },
  in_progress: { label: 'В процессе', color: 'warning' },
  ready: { label: 'Готовы', color: 'blue' },
  issued: { label: 'Выданы', color: 'success' },
}

export default function PlanDosmorovPage() {
  const { user } = useAuthStore()
  const isAuthenticated = !!user

  const [records, setRecords] = useState<InspectionRecord[]>([])
  const [loading, setLoading] = useState(true)
  const [open, setOpen] = useState(false)
  const [editingId, setEditingId] = useState<number | null>(null)
  const [saving, setSaving] = useState(false)
  const [form] = Form.useForm()

  const [search, setSearch] = useState('')
  const [filterManager, setFilterManager] = useState('')
  const [filterDateFrom, setFilterDateFrom] = useState<string>('')
  const [filterDateTo, setFilterDateTo] = useState<string>('')

  const load = () => {
    setLoading(true)
    const params: Record<string, string> = {}
    if (filterManager) params.manager = filterManager
    if (filterDateFrom) params.date_from = filterDateFrom
    if (filterDateTo) params.date_to = filterDateTo
    inspectionRecordsApi.list(params)
      .then(({ data }) => setRecords(data))
      .catch(() => {})
      .finally(() => setLoading(false))
  }

  useEffect(() => { load() }, [filterManager, filterDateFrom, filterDateTo])

  const filtered = search
    ? records.filter((r) =>
        [r.client, r.manager, r.commodity, r.pod, r.terminal, r.number]
          .some((v) => v?.toLowerCase().includes(search.toLowerCase()))
      )
    : records

  const openNew = () => {
    setEditingId(null)
    form.resetFields()
    setOpen(true)
  }

  const openEdit = (r: InspectionRecord) => {
    setEditingId(r.id!)
    form.setFieldsValue({
      ...r,
      inspection_date_plan: r.inspection_date_plan ? dayjs(r.inspection_date_plan) : null,
      fss_date_plan: r.fss_date_plan ? dayjs(r.fss_date_plan) : null,
    })
    setOpen(true)
  }

  const onSave = async () => {
    const values = await form.validateFields()
    if (values.inspection_date_plan) values.inspection_date_plan = values.inspection_date_plan.format('YYYY-MM-DD')
    if (values.fss_date_plan) values.fss_date_plan = values.fss_date_plan.format('YYYY-MM-DD')
    setSaving(true)
    try {
      if (editingId) {
        await inspectionRecordsApi.update(editingId, values)
      } else {
        await inspectionRecordsApi.create(values)
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

  const onDelete = async (id: number) => {
    try {
      await inspectionRecordsApi.remove(id)
      message.success('Удалено')
      load()
    } catch {
      message.error('Ошибка удаления')
    }
  }

  const columns: ColumnsType<InspectionRecord> = [
    {
      title: '№', dataIndex: 'number', key: 'number', width: 80, fixed: 'left',
      render: (v) => <b>{v}</b>,
    },
    { title: 'Клиент', dataIndex: 'client', key: 'client', width: 160, ellipsis: true },
    { title: 'Менеджер', dataIndex: 'manager', key: 'manager', width: 120, ellipsis: true },
    {
      title: 'Культура', dataIndex: 'commodity', key: 'commodity', width: 130,
      render: (v) => v ? <Tag color="green">{v}</Tag> : '—',
    },
    {
      title: 'Кол-во', dataIndex: 'container_count', key: 'container_count', width: 90,
      align: 'center',
    },
    {
      title: 'Вес (кг)', dataIndex: 'weight', key: 'weight', width: 110,
      align: 'right',
      render: (v) => v ? Number(v).toLocaleString('ru-RU') : '—',
    },
    { title: 'POD', dataIndex: 'pod', key: 'pod', width: 130, ellipsis: true },
    { title: 'Терминал', dataIndex: 'terminal', key: 'terminal', width: 130, ellipsis: true },
    {
      title: 'Карантинки', dataIndex: 'quarantine', key: 'quarantine', width: 120,
      align: 'center',
      render: (v) => {
        const s = QUARANTINE_LABELS[v]
        return s ? <Tag color={s.color}>{s.label}</Tag> : '—'
      },
    },
    {
      title: 'ДОСМОТР (ПЛАН)', dataIndex: 'inspection_date_plan', key: 'inspection_date_plan',
      width: 150, align: 'center',
      render: (v) => v ? (
        <span style={{ fontWeight: 600, color: '#1a3c6e' }}>{dayjs(v).format('DD.MM.YYYY')}</span>
      ) : '—',
    },
    {
      title: 'Дата выдачи ФСС (ПЛАН)', dataIndex: 'fss_date_plan', key: 'fss_date_plan',
      width: 170, align: 'center',
      render: (v) => v ? dayjs(v).format('DD.MM.YYYY') : '—',
    },
    {
      title: 'Груз', dataIndex: 'cargo_status', key: 'cargo_status', width: 110,
      align: 'center',
      render: (v) => {
        const s = CARGO_STATUS_LABELS[v]
        return s ? <Tag color={s.color}>{s.label}</Tag> : '—'
      },
    },
    {
      title: 'Документы', dataIndex: 'documents_status', key: 'documents_status', width: 120,
      align: 'center',
      render: (v) => {
        const s = DOC_STATUS_LABELS[v]
        return s ? <Tag color={s.color}>{s.label}</Tag> : '—'
      },
    },
    {
      title: 'Комментарии', dataIndex: 'comments', key: 'comments', width: 200, ellipsis: true,
      render: (v) => v ? <Tooltip title={v}><span>{v}</span></Tooltip> : '',
    },
    {
      title: '', key: 'actions', width: 80, fixed: 'right',
      render: (_: unknown, r: InspectionRecord) => (
        <Space size={4}>
          <Button size="small" icon={<EditOutlined />} onClick={() => openEdit(r)} />
          <Popconfirm title="Удалить запись?" onConfirm={() => onDelete(r.id!)} okText="Да" cancelText="Нет">
            <Button size="small" danger icon={<DeleteOutlined />} />
          </Popconfirm>
        </Space>
      ),
    },
  ]

  return (
    <>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
        <div>
          <Typography.Title level={4} style={{ margin: 0, color: '#1a3c6e' }}>
            План досмотров
          </Typography.Title>
          <Typography.Text type="secondary">
            Оперативное планирование инспекций и выдачи ФСС
          </Typography.Text>
        </div>
        <Space>
          <Button icon={<ReloadOutlined />} onClick={load}>Обновить</Button>
          {isAuthenticated && (
            <Button type="primary" icon={<PlusOutlined />} onClick={openNew}>
              Добавить
            </Button>
          )}
        </Space>
      </div>

      <Card size="small" style={{ marginBottom: 12 }}>
        <Space wrap>
          <Input
            prefix={<SearchOutlined />}
            placeholder="Поиск по клиенту, менеджеру, культуре, POD..."
            style={{ width: 340 }}
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            allowClear
          />
          <Input
            prefix={<FilterOutlined />}
            placeholder="Менеджер"
            style={{ width: 150 }}
            value={filterManager}
            onChange={(e) => setFilterManager(e.target.value)}
            allowClear
          />
          <DatePicker
            placeholder="ДОСМОТР от"
            format="DD.MM.YYYY"
            onChange={(d) => setFilterDateFrom(d ? d.format('YYYY-MM-DD') : '')}
          />
          <DatePicker
            placeholder="ДОСМОТР до"
            format="DD.MM.YYYY"
            onChange={(d) => setFilterDateTo(d ? d.format('YYYY-MM-DD') : '')}
          />
        </Space>
      </Card>

      <Card bodyStyle={{ padding: 0 }}>
        <Table<InspectionRecord>
          dataSource={filtered}
          columns={columns}
          rowKey="id"
          loading={loading}
          size="small"
          scroll={{ x: 1600 }}
          pagination={{
            pageSize: 25,
            showTotal: (t) => `Всего ${t} записей`,
            showSizeChanger: true,
            pageSizeOptions: ['25', '50', '100'],
          }}
          rowClassName={(r) => {
            if (r.inspection_date_plan && dayjs(r.inspection_date_plan).isBefore(dayjs(), 'day')
              && r.cargo_status === 'waiting') {
              return 'row-overdue'
            }
            return ''
          }}
          style={{ fontSize: 13 }}
        />
      </Card>

      <div style={{ marginTop: 8, display: 'flex', gap: 16, flexWrap: 'wrap' }}>
        <Typography.Text type="secondary" style={{ fontSize: 12 }}>
          <b>Груз:</b>{' '}
          {Object.values(CARGO_STATUS_LABELS).map((s) => (
            <Tag key={s.label} color={s.color} style={{ marginRight: 4, fontSize: 11 }}>{s.label}</Tag>
          ))}
        </Typography.Text>
        <Typography.Text type="secondary" style={{ fontSize: 12 }}>
          <b>Документы:</b>{' '}
          {Object.values(DOC_STATUS_LABELS).map((s) => (
            <Tag key={s.label} color={s.color} style={{ marginRight: 4, fontSize: 11 }}>{s.label}</Tag>
          ))}
        </Typography.Text>
      </div>

      <Modal
        title={editingId ? 'Редактировать запись' : 'Новая запись'}
        open={open}
        onCancel={() => setOpen(false)}
        onOk={onSave}
        okText="Сохранить"
        cancelText="Отмена"
        confirmLoading={saving}
        width={700}
        destroyOnClose
      >
        <Form form={form} layout="vertical" style={{ marginTop: 16 }}>
          <Space style={{ display: 'flex' }} align="start">
            <Form.Item label="№" name="number" style={{ width: 100 }}>
              <Input />
            </Form.Item>
            <Form.Item label="Клиент" name="client" style={{ width: 220 }}>
              <Input />
            </Form.Item>
            <Form.Item label="Менеджер" name="manager" style={{ width: 160 }}>
              <Input />
            </Form.Item>
          </Space>

          <Space style={{ display: 'flex' }} align="start">
            <Form.Item label="Культура" name="commodity" style={{ width: 160 }}>
              <Input />
            </Form.Item>
            <Form.Item label="Кол-во контейнеров" name="container_count" style={{ width: 160 }}>
              <Input placeholder="3×40HC" />
            </Form.Item>
            <Form.Item label="Вес (кг)" name="weight" style={{ width: 140 }}>
              <InputNumber style={{ width: '100%' }} step={1000} />
            </Form.Item>
          </Space>

          <Space style={{ display: 'flex' }} align="start">
            <Form.Item label="POD (порт назначения)" name="pod" style={{ width: 220 }}>
              <Input />
            </Form.Item>
            <Form.Item label="Терминал" name="terminal" style={{ width: 200 }}>
              <Input />
            </Form.Item>
          </Space>

          <Space style={{ display: 'flex' }} align="start">
            <Form.Item label="Карантинки" name="quarantine" style={{ width: 160 }}>
              <Select allowClear options={[
                { value: 'own', label: 'Свои' },
                { value: 'client', label: 'Клиентские' },
                { value: 'shared', label: 'Совместные' },
                { value: 'other', label: 'Другое' },
              ]} />
            </Form.Item>
            <Form.Item label="ДОСМОТР (ПЛАН)" name="inspection_date_plan" style={{ width: 180 }}>
              <DatePicker format="DD.MM.YYYY" style={{ width: '100%' }} />
            </Form.Item>
            <Form.Item label="Дата выдачи ФСС (ПЛАН)" name="fss_date_plan" style={{ width: 200 }}>
              <DatePicker format="DD.MM.YYYY" style={{ width: '100%' }} />
            </Form.Item>
          </Space>

          <Space style={{ display: 'flex' }} align="start">
            <Form.Item label="Статус груза" name="cargo_status" style={{ width: 190 }}>
              <Select options={[
                { value: 'waiting', label: 'Ожидает' },
                { value: 'loaded', label: 'Погружен' },
                { value: 'shipped', label: 'Отгружен' },
                { value: 'on_way', label: 'В пути' },
                { value: 'delivered', label: 'Доставлен' },
              ]} />
            </Form.Item>
            <Form.Item label="Статус документов" name="documents_status" style={{ width: 190 }}>
              <Select options={[
                { value: 'not_ready', label: 'Не готовы' },
                { value: 'in_progress', label: 'В процессе' },
                { value: 'ready', label: 'Готовы' },
                { value: 'issued', label: 'Выданы' },
              ]} />
            </Form.Item>
          </Space>

          <Form.Item label="Комментарии" name="comments">
            <Input.TextArea rows={3} />
          </Form.Item>
        </Form>
      </Modal>

      <style>{`
        .row-overdue td { background: #fff2f0 !important; }
        .row-overdue:hover td { background: #ffe7e4 !important; }
      `}</style>
    </>
  )
}
