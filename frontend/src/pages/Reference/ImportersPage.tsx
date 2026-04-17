import { Form, Input, Switch } from 'antd'
import ReferenceTable from '../../components/ReferenceTable'
import { importersApi } from '../../api/reference'
import type { Importer } from '../../types/reference'

const columns = [
  { title: 'Наименование (eng)', dataIndex: 'name_eng', key: 'name_eng', ellipsis: true },
  { title: 'Адрес (eng)', dataIndex: 'address_eng', key: 'address_eng', ellipsis: true },
  { title: 'Страна', dataIndex: 'country', key: 'country', width: 120 },
  { title: 'Город', dataIndex: 'city', key: 'city', width: 120 },
  { title: 'Активен', dataIndex: 'is_active', key: 'is_active', width: 80, render: (v: boolean) => v ? '✓' : '✗' },
]

const formFields = (
  <>
    <Form.Item label="Наименование (eng)" name="name_eng" rules={[{ required: true }]}><Input /></Form.Item>
    <Form.Item label="Адрес (eng)" name="address_eng"><Input /></Form.Item>
    <Form.Item label="Страна" name="country"><Input /></Form.Item>
    <Form.Item label="Город" name="city"><Input /></Form.Item>
    <Form.Item label="Активен" name="is_active" valuePropName="checked" initialValue={true}><Switch /></Form.Item>
  </>
)

export default function ImportersPage() {
  return <ReferenceTable<Importer> title="Импортёры" api={importersApi} columns={columns} formFields={formFields} />
}
