import { Form, Input, Switch } from 'antd'
import ReferenceTable from '../../components/ReferenceTable'
import { productsApi } from '../../api/reference'
import type { Product } from '../../types/reference'

const columns = [
  { title: 'Наименование (рус)', dataIndex: 'name_rus', key: 'name_rus', ellipsis: true },
  { title: 'Наименование (eng)', dataIndex: 'name_eng', key: 'name_eng', ellipsis: true },
  { title: 'Ботаническое название', dataIndex: 'botanical_name', key: 'botanical_name', ellipsis: true },
  { title: 'Код ТНВЭД', dataIndex: 'tnved_code', key: 'tnved_code', width: 120 },
  { title: 'Активен', dataIndex: 'is_active', key: 'is_active', width: 80, render: (v: boolean) => v ? '✓' : '✗' },
]

const formFields = (
  <>
    <Form.Item label="Наименование (рус)" name="name_rus" rules={[{ required: true }]}><Input /></Form.Item>
    <Form.Item label="Наименование (eng)" name="name_eng"><Input /></Form.Item>
    <Form.Item label="Ботаническое название" name="botanical_name"><Input /></Form.Item>
    <Form.Item label="Код ТНВЭД" name="tnved_code"><Input /></Form.Item>
    <Form.Item label="Активен" name="is_active" valuePropName="checked" initialValue={true}><Switch /></Form.Item>
  </>
)

export default function ProductsPage() {
  return <ReferenceTable<Product> title="Продукция" api={productsApi} columns={columns} formFields={formFields} />
}
