import { Form, Input, Select, Switch, Tag } from 'antd'
import ReferenceTable from '../../components/ReferenceTable'
import { counterpartiesApi } from '../../api/reference'
import type { Counterparty } from '../../types/reference'
import { useCanEdit, useCanAdd } from '../../hooks/useCanEdit'

const STATUS_OPTIONS = [
  { value: 'active', label: 'Активен' },
  { value: 'inactive', label: 'Неактивен' },
  { value: 'blocked', label: 'Заблокирован' },
]

const STATUS_COLOR: Record<string, string> = {
  active: 'green', inactive: 'default', blocked: 'red',
}

const columns = [
  { title: 'Наименование (рус)', dataIndex: 'name_ru', key: 'name_ru', ellipsis: true },
  { title: 'Наименование (eng)', dataIndex: 'name_en', key: 'name_en', ellipsis: true, render: (v: string | null) => v || '—' },
  { title: 'ИНН', dataIndex: 'inn', key: 'inn', width: 120, render: (v: string | null) => v || '—' },
  { title: 'КПП', dataIndex: 'kpp', key: 'kpp', width: 100, render: (v: string | null) => v || '—' },
  {
    title: 'Статус', dataIndex: 'status_code', key: 'status_code', width: 110,
    render: (v: string) => <Tag color={STATUS_COLOR[v] || 'default'}>{STATUS_OPTIONS.find(o => o.value === v)?.label ?? v}</Tag>,
  },
  {
    title: 'Активен', dataIndex: 'is_active', key: 'is_active', width: 80,
    render: (v: boolean) => <Tag color={v ? 'green' : 'default'}>{v ? 'Да' : 'Нет'}</Tag>,
  },
]

const formFields = (
  <>
    <Form.Item label="Наименование (рус)" name="name_ru" rules={[{ required: true, message: 'Обязательно' }]}>
      <Input />
    </Form.Item>
    <Form.Item label="Наименование (eng)" name="name_en">
      <Input />
    </Form.Item>
    <div style={{ display: 'flex', gap: 8 }}>
      <Form.Item label="ИНН" name="inn" style={{ flex: 1 }}
        rules={[{ pattern: /^\d{10}$|^\d{12}$/, message: '10 или 12 цифр' }]}>
        <Input maxLength={12} />
      </Form.Item>
      <Form.Item label="КПП" name="kpp" style={{ flex: 1 }}
        rules={[{ pattern: /^\d{9}$/, message: '9 цифр' }]}>
        <Input maxLength={9} />
      </Form.Item>
      <Form.Item label="ОГРН" name="ogrn" style={{ flex: 1 }}
        rules={[{ pattern: /^\d{13}$|^\d{15}$/, message: '13 или 15 цифр' }]}>
        <Input maxLength={15} />
      </Form.Item>
    </div>
    <Form.Item label="Юридический адрес (рус)" name="legal_address_ru">
      <Input.TextArea rows={2} />
    </Form.Item>
    <Form.Item label="Фактический адрес (рус)" name="actual_address_ru">
      <Input.TextArea rows={2} />
    </Form.Item>
    <Form.Item label="Юридический адрес (eng)" name="legal_address_en">
      <Input.TextArea rows={2} />
    </Form.Item>
    <Form.Item label="Фактический адрес (eng)" name="actual_address_en">
      <Input.TextArea rows={2} />
    </Form.Item>
    <div style={{ display: 'flex', gap: 8 }}>
      <Form.Item label="Статус" name="status_code" initialValue="active" style={{ flex: 1 }}>
        <Select options={STATUS_OPTIONS} />
      </Form.Item>
      <Form.Item label="Активен" name="is_active" valuePropName="checked" initialValue={true} style={{ flex: 0 }}>
        <Switch />
      </Form.Item>
    </div>
  </>
)

export default function CounterpartiesPage() {
  const canEdit = useCanEdit()
  const canAdd = useCanAdd()
  return (
    <ReferenceTable<Counterparty>
      title="Контрагенты"
      api={counterpartiesApi}
      columns={columns}
      formFields={formFields}
      canEdit={canEdit}
      canAdd={canAdd}
      listParams={{ active_only: 'false' }}
      modalWidth={640}
    />
  )
}
