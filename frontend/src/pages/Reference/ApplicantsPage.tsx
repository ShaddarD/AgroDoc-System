import { Form, Input, Switch } from 'antd'
import ReferenceTable from '../../components/ReferenceTable'
import { applicantsApi } from '../../api/reference'
import type { Applicant } from '../../types/reference'

const columns = [
  { title: 'Наименование (рус)', dataIndex: 'name_rus', key: 'name_rus', ellipsis: true },
  { title: 'Наименование (eng)', dataIndex: 'name_eng', key: 'name_eng', ellipsis: true },
  { title: 'ИНН', dataIndex: 'inn', key: 'inn', width: 120 },
  { title: 'Телефон', dataIndex: 'phone', key: 'phone', width: 140 },
  { title: 'Активен', dataIndex: 'is_active', key: 'is_active', width: 80, render: (v: boolean) => v ? '✓' : '✗' },
]

const formFields = (
  <>
    <Form.Item label="Наименование (рус)" name="name_rus" rules={[{ required: true }]}><Input /></Form.Item>
    <Form.Item label="Наименование (eng)" name="name_eng"><Input /></Form.Item>
    <Form.Item label="Юридический адрес" name="legal_address"><Input /></Form.Item>
    <Form.Item label="Фактический адрес" name="actual_address"><Input /></Form.Item>
    <Form.Item label="ИНН" name="inn"><Input /></Form.Item>
    <Form.Item label="КПП" name="kpp"><Input /></Form.Item>
    <Form.Item label="ОГРН" name="ogrn"><Input /></Form.Item>
    <Form.Item label="Контактное лицо" name="contact_person"><Input /></Form.Item>
    <Form.Item label="Телефон" name="phone"><Input /></Form.Item>
    <Form.Item label="Email" name="email"><Input type="email" /></Form.Item>
    <Form.Item label="Активен" name="is_active" valuePropName="checked" initialValue={true}><Switch /></Form.Item>
  </>
)

export default function ApplicantsPage() {
  return <ReferenceTable<Applicant> title="Заявители" api={applicantsApi} columns={columns} formFields={formFields} />
}
