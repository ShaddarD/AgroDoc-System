import { Form, Input, Switch } from 'antd'
import ReferenceTable from '../../components/ReferenceTable'
import { inspectionPlacesApi } from '../../api/reference'
import type { InspectionPlace } from '../../types/reference'

const columns = [
  { title: 'Наименование', dataIndex: 'name', key: 'name', ellipsis: true },
  { title: 'Адрес', dataIndex: 'address', key: 'address', ellipsis: true },
  { title: 'Активен', dataIndex: 'is_active', key: 'is_active', width: 80, render: (v: boolean) => v ? '✓' : '✗' },
]

const formFields = (
  <>
    <Form.Item label="Наименование" name="name" rules={[{ required: true }]}><Input /></Form.Item>
    <Form.Item label="Адрес" name="address"><Input /></Form.Item>
    <Form.Item label="Активен" name="is_active" valuePropName="checked" initialValue={true}><Switch /></Form.Item>
  </>
)

export default function InspectionPlacesPage() {
  return <ReferenceTable<InspectionPlace> title="Места досмотра" api={inspectionPlacesApi} columns={columns} formFields={formFields} />
}
