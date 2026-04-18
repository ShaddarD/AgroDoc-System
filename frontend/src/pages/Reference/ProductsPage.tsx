import { Form, Input, Switch, Tag } from 'antd'
import ReferenceTable from '../../components/ReferenceTable'
import { productsApi } from '../../api/reference'
import type { Product } from '../../types/reference'
import { useCanEdit, useCanAdd } from '../../hooks/useCanEdit'

const columns = [
  { title: 'Код', dataIndex: 'product_code', key: 'product_code', width: 100 },
  { title: 'Код ТН ВЭД', dataIndex: 'hs_code_tnved', key: 'hs_code_tnved', width: 120 },
  { title: 'Наименование (рус)', dataIndex: 'name_ru', key: 'name_ru', ellipsis: true },
  { title: 'Наименование (eng)', dataIndex: 'name_en', key: 'name_en', ellipsis: true, render: (v: string | null) => v || '—' },
  { title: 'Ботаническое название', dataIndex: 'botanical_name_latin', key: 'botanical_name_latin', ellipsis: true, render: (v: string | null) => v ? <i>{v}</i> : '—' },
  {
    title: 'Активен', dataIndex: 'is_active', key: 'is_active', width: 80,
    render: (v: boolean) => <Tag color={v ? 'green' : 'default'}>{v ? 'Да' : 'Нет'}</Tag>,
  },
]

const formFields = (
  <>
    <div style={{ display: 'flex', gap: 8 }}>
      <Form.Item label="Код продукта" name="product_code" rules={[{ required: true, message: 'Обязательно' }]} style={{ flex: 1 }}>
        <Input />
      </Form.Item>
      <Form.Item label="Код ТН ВЭД" name="hs_code_tnved" rules={[{ required: true, message: 'Обязательно' }, { pattern: /^\d+$/, message: 'Только цифры' }]} style={{ flex: 1 }}>
        <Input maxLength={20} />
      </Form.Item>
    </div>
    <Form.Item label="Наименование (рус)" name="name_ru" rules={[{ required: true, message: 'Обязательно' }]}>
      <Input />
    </Form.Item>
    <Form.Item label="Наименование (eng)" name="name_en">
      <Input />
    </Form.Item>
    <Form.Item label="Ботаническое название (латынь)" name="botanical_name_latin">
      <Input />
    </Form.Item>
    <Form.Item label="Нормативные документы" name="regulatory_documents">
      <Input.TextArea rows={3} />
    </Form.Item>
    <Form.Item label="Активен" name="is_active" valuePropName="checked" initialValue={true}>
      <Switch />
    </Form.Item>
  </>
)

export default function ProductsPage() {
  const canEdit = useCanEdit()
  const canAdd = useCanAdd()
  return (
    <ReferenceTable<Product>
      title="Продукция"
      api={productsApi}
      columns={columns}
      formFields={formFields}
      canEdit={canEdit}
      canAdd={canAdd}
      listParams={{ active_only: 'false' }}
      modalWidth={580}
    />
  )
}
