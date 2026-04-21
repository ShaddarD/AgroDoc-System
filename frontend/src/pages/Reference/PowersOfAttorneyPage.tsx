import { useEffect, useState } from 'react'
import { Form, Input, InputNumber, Select, Switch, Tag } from 'antd'
import dayjs from 'dayjs'
import ReferenceTable from '../../components/ReferenceTable'
import { powersOfAttorneyApi, counterpartiesApi } from '../../api/reference'
import type { PowerOfAttorney, Counterparty } from '../../types/reference'
import { useCanEdit, useCanAdd } from '../../hooks/useCanEdit'

const STATUS_OPTIONS = [
  { value: 'active', label: 'Действует' },
  { value: 'revoked', label: 'Отозвана' },
  { value: 'inactive', label: 'Неактивна' },
  { value: 'draft', label: 'Черновик' },
]
const STATUS_COLOR: Record<string, string> = {
  active: 'green', revoked: 'red', inactive: 'default', draft: 'orange',
}

export default function PowersOfAttorneyPage() {
  const canEdit = useCanEdit()
  const canAdd = useCanAdd()
  const [counterpartyOptions, setCounterpartyOptions] = useState<{ value: string; label: string }[]>([])

  useEffect(() => {
    counterpartiesApi.list({ active_only: 'false' }).then(({ data }) =>
      setCounterpartyOptions((data as Counterparty[]).map(c => ({ value: c.uuid, label: c.name_ru })))
    )
  }, [])

  const columns = [
    { title: '№ доверенности', dataIndex: 'poa_number', key: 'poa_number', width: 140 },
    {
      title: 'Дата выдачи', dataIndex: 'issue_date', key: 'issue_date', width: 120,
      render: (v: string) => v ? dayjs(v).format('DD.MM.YYYY') : '—',
    },
    {
      title: 'Истекает', dataIndex: 'expiry_date', key: 'expiry_date', width: 120,
      render: (v: string | null) => {
        if (!v) return '—'
        const expired = dayjs(v).isBefore(dayjs())
        return <span style={{ color: expired ? '#cf1322' : undefined }}>{dayjs(v).format('DD.MM.YYYY')}</span>
      },
    },
    {
      title: 'Принципал', dataIndex: 'principal_counterparty_name', key: 'principal_counterparty_name',
      ellipsis: true, render: (v: string | null) => v || '—',
    },
    {
      title: 'Поверенный', dataIndex: 'attorney_counterparty_name', key: 'attorney_counterparty_name',
      width: 160, render: (v: string | null) => v || '—',
    },
    {
      title: 'Статус', dataIndex: 'status_code', key: 'status_code', width: 110,
      render: (v: string) => <Tag color={STATUS_COLOR[v] || 'default'}>{STATUS_OPTIONS.find(o => o.value === v)?.label ?? v}</Tag>,
    },
  ]

  const formFields = (
    <>
      <div style={{ display: 'flex', gap: 8 }}>
        <Form.Item label="Номер доверенности" name="poa_number" rules={[{ required: true, message: 'Обязательно' }]} style={{ flex: 1 }}>
          <Input />
        </Form.Item>
        <Form.Item label="Дата выдачи" name="issue_date" rules={[{ required: true, message: 'Обязательно' }]} style={{ flex: 1 }}>
          <Input type="date" />
        </Form.Item>
      </div>
      <div style={{ display: 'flex', gap: 8 }}>
        <Form.Item label="Срок действия (лет)" name="validity_years" rules={[{ required: true, message: 'Обязательно' }]} style={{ flex: 1 }}>
          <InputNumber min={1} max={99} style={{ width: '100%' }} />
        </Form.Item>
        <Form.Item label="Статус" name="status_code" initialValue="active" style={{ flex: 1 }}>
          <Select options={STATUS_OPTIONS} />
        </Form.Item>
      </div>
      <Form.Item label="Принципал (контрагент)" name="principal_counterparty">
        <Select
          showSearch allowClear
          placeholder="Выберите контрагента"
          options={counterpartyOptions}
          filterOption={(input, option) =>
            (option?.label ?? '').toLowerCase().includes(input.toLowerCase())
          }
        />
      </Form.Item>
      <Form.Item label="Поверенный (контрагент)" name="attorney_counterparty">
        <Select
          showSearch allowClear
          placeholder="Выберите контрагента"
          options={counterpartyOptions}
          filterOption={(input, option) =>
            (option?.label ?? '').toLowerCase().includes(input.toLowerCase())
          }
        />
      </Form.Item>
      <Form.Item label="Активна" name="is_active" valuePropName="checked" initialValue={true}>
        <Switch />
      </Form.Item>
    </>
  )

  return (
    <ReferenceTable<PowerOfAttorney>
      title="Доверенности"
      api={powersOfAttorneyApi}
      columns={columns}
      formFields={formFields}
      canEdit={canEdit}
      canAdd={canAdd}
      listParams={{ active_only: 'false' }}
      modalWidth={600}
    />
  )
}
