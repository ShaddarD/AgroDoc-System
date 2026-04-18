import { useEffect, useState } from 'react'
import { Form, Input, Select, Switch, Tag } from 'antd'
import ReferenceTable from '../../components/ReferenceTable'
import { terminalsApi, counterpartiesApi } from '../../api/reference'
import type { Terminal, Counterparty } from '../../types/reference'
import { useCanEdit, useCanAdd } from '../../hooks/useCanEdit'

export default function TerminalsPage() {
  const canEdit = useCanEdit()
  const canAdd = useCanAdd()
  const [counterpartyOptions, setCounterpartyOptions] = useState<{ value: string; label: string }[]>([])

  useEffect(() => {
    counterpartiesApi.list({ active_only: 'true' }).then(({ data }) =>
      setCounterpartyOptions(data.map((c: Counterparty) => ({ value: c.uuid, label: c.name_ru })))
    )
  }, [])

  const columns = [
    { title: 'Код', dataIndex: 'terminal_code', key: 'terminal_code', width: 100 },
    { title: 'Наименование', dataIndex: 'terminal_name', key: 'terminal_name', ellipsis: true },
    {
      title: 'Владелец', dataIndex: 'owner_counterparty_name', key: 'owner_counterparty_name',
      ellipsis: true, render: (v: string | null) => v || '—',
    },
    { title: 'Адрес (рус)', dataIndex: 'address_ru', key: 'address_ru', ellipsis: true },
    {
      title: 'Активен', dataIndex: 'is_active', key: 'is_active', width: 80,
      render: (v: boolean) => <Tag color={v ? 'green' : 'default'}>{v ? 'Да' : 'Нет'}</Tag>,
    },
  ]

  const formFields = (
    <>
      <div style={{ display: 'flex', gap: 8 }}>
        <Form.Item label="Код терминала" name="terminal_code" rules={[{ required: true, message: 'Обязательно' }]} style={{ flex: 1 }}>
          <Input />
        </Form.Item>
        <Form.Item label="Наименование" name="terminal_name" rules={[{ required: true, message: 'Обязательно' }]} style={{ flex: 2 }}>
          <Input />
        </Form.Item>
      </div>
      <Form.Item label="Владелец (контрагент)" name="owner_counterparty">
        <Select
          showSearch
          allowClear
          placeholder="Выберите контрагента"
          options={counterpartyOptions}
          filterOption={(input, option) =>
            (option?.label ?? '').toLowerCase().includes(input.toLowerCase())
          }
        />
      </Form.Item>
      <Form.Item label="Адрес (рус)" name="address_ru" rules={[{ required: true, message: 'Обязательно' }]}>
        <Input.TextArea rows={2} />
      </Form.Item>
      <Form.Item label="Адрес (eng)" name="address_en">
        <Input.TextArea rows={2} />
      </Form.Item>
      <Form.Item label="Активен" name="is_active" valuePropName="checked" initialValue={true}>
        <Switch />
      </Form.Item>
    </>
  )

  return (
    <ReferenceTable<Terminal>
      title="Терминалы"
      api={terminalsApi}
      columns={columns}
      formFields={formFields}
      canEdit={canEdit}
      canAdd={canAdd}
      listParams={{ active_only: 'false' }}
      modalWidth={580}
    />
  )
}
