import { useEffect, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import {
  Button, Card, Checkbox, Col, Divider, Form, Input, InputNumber,
  message, Row, Select, Space, Spin, Tag, Tooltip, Typography,
} from 'antd'
import {
  SaveOutlined, ArrowLeftOutlined, FileWordOutlined,
  FileExcelOutlined, UploadOutlined,
} from '@ant-design/icons'
import { applicationsApi } from '../../api/applications'
import { applicantsApi, productsApi, importersApi, inspectionPlacesApi } from '../../api/reference'
import type { Applicant, Product, Importer, InspectionPlace } from '../../types/reference'
import type { Application, GeneratedFile } from '../../types/application'
import { useAuthStore } from '../../store/authStore'

const CERTIFICATE_OPTIONS = [
  { label: 'Сертификат безопасности и качества', value: 'safety_quality' },
  { label: 'Сертификат здоровья', value: 'health' },
  { label: 'Международный сертификат качества', value: 'intl_quality' },
  { label: 'Радиологический сертификат', value: 'radio' },
  { label: 'Сертификат ГМО', value: 'gmo' },
]

export default function ApplicationFormPage() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const [form] = Form.useForm()
  const isNew = !id || id === 'new'
  const user = useAuthStore((s) => s.user)

  const [loading, setLoading] = useState(!isNew)
  const [saving, setSaving] = useState(false)
  const [generating, setGenerating] = useState(false)
  const [files, setFiles] = useState<GeneratedFile[]>([])

  const [applicants, setApplicants] = useState<Applicant[]>([])
  const [products, setProducts] = useState<Product[]>([])
  const [importers, setImporters] = useState<Importer[]>([])
  const [inspectionPlaces, setInspectionPlaces] = useState<InspectionPlace[]>([])

  const [appNumber, setAppNumber] = useState('')
  const [status, setStatus] = useState('draft')

  useEffect(() => {
    Promise.all([
      applicantsApi.list(),
      productsApi.list(),
      importersApi.list(),
      inspectionPlacesApi.list(),
    ]).then(([a, p, i, ip]) => {
      const activeApplicants = a.data.filter((x) => x.is_active)
      setApplicants(activeApplicants)
      setProducts(p.data.filter((x) => x.is_active))
      setImporters(i.data.filter((x) => x.is_active))
      setInspectionPlaces(ip.data.filter((x) => x.is_active))

      // Авто-выбор заявителя по ИНН залогиненного пользователя
      if (isNew && user?.inn) {
        const matched = activeApplicants.find((a) => a.inn === user.inn)
        if (matched) {
          form.setFieldValue('applicant', matched.id)
          fillExporterFields(matched)
        }
      }
    })

    if (!isNew) {
      applicationsApi.get(id!).then(({ data }) => {
        form.setFieldsValue({ ...data })
        setAppNumber(data.application_number)
        setStatus(data.status ?? 'draft')
        return applicationsApi.getFiles(id!)
      }).then(({ data }) => setFiles(data))
        .finally(() => setLoading(false))
    }
  }, [id])

  const fillExporterFields = (a: Applicant) => {
    form.setFieldsValue({
      exporter_rus: a.name_rus,
      exporter_eng: a.name_eng,
      exporter_address: a.legal_address,
      exporter_inn: a.inn,
      exporter_kpp: a.kpp,
      exporter_ogrn: a.ogrn,
    })
  }

  const onApplicantChange = (val: string) => {
    const a = applicants.find((x) => x.id === val)
    if (a) fillExporterFields(a)
  }

  const onExporterSelectChange = (val: string) => {
    const a = applicants.find((x) => x.id === val)
    if (a) fillExporterFields(a)
  }

  const onProductChange = (val: string) => {
    const p = products.find((x) => x.id === val)
    if (p) {
      form.setFieldsValue({
        product_rus: p.name_rus || p.name_ru,
        product_eng: p.name_eng,
        botanical_name: p.botanical_name,
        tnved_code: p.tnved_code,
      })
    }
  }

  const onSave = async () => {
    try {
      const values = await form.validateFields()
      setSaving(true)
      if (isNew) {
        const { data } = await applicationsApi.create(values)
        message.success('Заявка создана')
        navigate(`/applications/${data.id}/edit`)
      } else {
        await applicationsApi.update(id!, values)
        message.success('Заявка сохранена')
      }
    } catch (e: any) {
      if (e?.errorFields) return
      message.error('Ошибка сохранения')
    } finally {
      setSaving(false)
    }
  }

  const onGenerate = async (docTypes: string[]) => {
    setGenerating(true)
    try {
      const { data } = await applicationsApi.generateDocuments(id!, docTypes)
      setFiles((prev) => [...prev, ...data])
      message.success(`Сгенерировано: ${data.map((f) => f.file_name).join(', ')}`)
    } catch {
      message.error('Ошибка генерации документов')
    } finally {
      setGenerating(false)
    }
  }

  const downloadFile = async (file: GeneratedFile) => {
    const { data } = await applicationsApi.downloadFile(file.id)
    const url = URL.createObjectURL(new Blob([data]))
    const a = document.createElement('a')
    a.href = url
    a.download = file.file_name
    a.click()
    URL.revokeObjectURL(url)
  }

  if (loading) return <Spin size="large" style={{ display: 'block', textAlign: 'center', marginTop: 80 }} />

  const title = isNew ? 'Новая заявка' : `Заявка № ${appNumber}`

  return (
    <>
      {/* ── ШАПКА ── */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16, flexWrap: 'wrap', gap: 8 }}>
        <Space wrap>
          <Button icon={<ArrowLeftOutlined />} onClick={() => navigate('/applications')} />
          <Typography.Title level={4} style={{ margin: 0 }}>{title}</Typography.Title>
          {status && (
            <Tag color={status === 'completed' ? 'success' : status === 'archived' ? 'orange' : 'default'}>
              {status === 'draft' ? 'Черновик' : status === 'completed' ? 'Завершена' : 'Архив'}
            </Tag>
          )}
        </Space>
        <Space wrap>
          {!isNew && (
            <>
              <Button icon={<FileWordOutlined />} loading={generating} onClick={() => onGenerate(['cokz'])}>СОКЗ</Button>
              <Button icon={<FileExcelOutlined />} loading={generating} onClick={() => onGenerate(['fito1', 'fito2'])}>ФИТО</Button>
              <Button icon={<FileExcelOutlined />} loading={generating} onClick={() => onGenerate(['act'])}>АКТ</Button>
              <Button onClick={() => onGenerate(['cokz', 'fito1', 'fito2', 'act'])} loading={generating}>Все документы</Button>
            </>
          )}
          <Button type="primary" icon={<SaveOutlined />} loading={saving} onClick={onSave}>Сохранить</Button>
        </Space>
      </div>

      <Form form={form} layout="vertical" size="middle">

        {/* ── НОМЕР АКТА ── */}
        <Card style={{ marginBottom: 16 }}>
          <Row gutter={16}>
            <Col xs={24} md={8}>
              <Form.Item label="Номер акта" name="act_number">
                <Input placeholder="Введите номер акта вручную" />
              </Form.Item>
            </Col>
          </Row>
        </Card>

        {/* ── ЗАЯВИТЕЛЬ ── */}
        <Card title="Заявитель" style={{ marginBottom: 16 }}>
          <Row gutter={16}>
            <Col xs={24} md={12}>
              <Form.Item label="Заявитель из справочника" name="applicant">
                <Select
                  showSearch
                  placeholder="Выберите заявителя"
                  allowClear
                  filterOption={(input, option) =>
                    (option?.label as string)?.toLowerCase().includes(input.toLowerCase())
                  }
                  onChange={onApplicantChange}
                  options={applicants.map((a) => ({ value: a.id, label: `${a.name_rus} (ИНН: ${a.inn})` }))}
                />
              </Form.Item>
            </Col>
            <Col xs={24} md={12}>
              <Form.Item label="Заявитель (вручную)" name="applicant_custom">
                <Input placeholder="Если нет в справочнике" />
              </Form.Item>
            </Col>
            <Col xs={24} md={12}>
              <Form.Item label="Поручение №" name="poruchenie">
                <Input />
              </Form.Item>
            </Col>
            <Col xs={24} md={12}>
              <Form.Item label="Доверенность №" name="doverennost">
                <Input />
              </Form.Item>
            </Col>
          </Row>
        </Card>

        {/* ── ЭКСПОРТЁР ── */}
        <Card title="Экспортёр" style={{ marginBottom: 16 }}>
          <Row gutter={16}>
            <Col xs={24} md={12}>
              <Form.Item label="Выбрать из справочника (поиск по ИНН или названию)" name="exporter_ref">
                <Select
                  showSearch
                  placeholder="Начните вводить ИНН или название"
                  allowClear
                  filterOption={(input, option) =>
                    (option?.label as string)?.toLowerCase().includes(input.toLowerCase())
                  }
                  onChange={onExporterSelectChange}
                  options={applicants.map((a) => ({ value: a.id, label: `${a.inn} — ${a.name_rus}` }))}
                />
              </Form.Item>
            </Col>
            <Col xs={24} md={12}><Form.Item label="Наименование (рус)" name="exporter_rus"><Input /></Form.Item></Col>
            <Col xs={24} md={12}><Form.Item label="Наименование (eng)" name="exporter_eng"><Input /></Form.Item></Col>
            <Col xs={24} md={24}><Form.Item label="Адрес" name="exporter_address"><Input /></Form.Item></Col>
            <Col xs={24} md={8}><Form.Item label="ИНН" name="exporter_inn"><Input /></Form.Item></Col>
            <Col xs={24} md={8}><Form.Item label="КПП" name="exporter_kpp"><Input /></Form.Item></Col>
            <Col xs={24} md={8}><Form.Item label="ОГРН" name="exporter_ogrn"><Input /></Form.Item></Col>
          </Row>
        </Card>

        {/* ── ИМПОРТЁР ── */}
        <Card title="Импортёр" style={{ marginBottom: 16 }}>
          <Row gutter={16}>
            <Col xs={24} md={12}>
              <Form.Item label="Импортёр из справочника" name="importer">
                <Select
                  showSearch
                  placeholder="Выберите импортёра"
                  allowClear
                  filterOption={(input, option) =>
                    (option?.label as string)?.toLowerCase().includes(input.toLowerCase())
                  }
                  options={importers.map((x) => ({ value: x.id, label: x.name_eng }))}
                />
              </Form.Item>
            </Col>
            <Col xs={24} md={12}><Form.Item label="Импортёр (вручную)" name="importer_custom"><Input /></Form.Item></Col>
            <Col xs={24} md={12}><Form.Item label="Наименование (eng)" name="importer_name_eng"><Input /></Form.Item></Col>
            <Col xs={24} md={12}><Form.Item label="Адрес (eng)" name="importer_address_eng"><Input /></Form.Item></Col>
          </Row>
        </Card>

        {/* ── ПРОДУКЦИЯ ── */}
        <Card title="Продукция" style={{ marginBottom: 16 }}>
          <Row gutter={16}>
            <Col xs={24} md={12}>
              <Form.Item label="Продукция из справочника" name="product">
                <Select
                  showSearch
                  placeholder="Выберите продукцию"
                  allowClear
                  filterOption={(input, option) =>
                    (option?.label as string)?.toLowerCase().includes(input.toLowerCase())
                  }
                  onChange={onProductChange}
                  options={products.map((x) => ({ value: x.id, label: x.name_rus }))}
                />
              </Form.Item>
            </Col>
            <Col xs={24} md={12}><Form.Item label="Продукция (вручную)" name="product_custom"><Input /></Form.Item></Col>
            <Col xs={24} md={12}><Form.Item label="Наименование (рус)" name="product_rus"><Input /></Form.Item></Col>
            <Col xs={24} md={12}><Form.Item label="Наименование (eng)" name="product_eng"><Input /></Form.Item></Col>
            <Col xs={24} md={12}><Form.Item label="Ботаническое название" name="botanical_name"><Input /></Form.Item></Col>
            <Col xs={24} md={12}><Form.Item label="Код ТНВЭД" name="tnved_code"><Input /></Form.Item></Col>
          </Row>
        </Card>

        {/* ── ГРУЗ ── */}
        <Card title="Груз и отгрузка" style={{ marginBottom: 16 }}>
          <Row gutter={16}>
            <Col xs={24} md={8}><Form.Item label="Вес (тонн)" name="weight_tons"><InputNumber style={{ width: '100%' }} step={0.001} /></Form.Item></Col>
            <Col xs={24} md={8}><Form.Item label="Вес (MT)" name="weight_mt"><InputNumber style={{ width: '100%' }} step={0.001} /></Form.Item></Col>
            <Col xs={24} md={8}><Form.Item label="Количество мест" name="places_count"><InputNumber style={{ width: '100%' }} /></Form.Item></Col>
            <Col xs={24} md={12}><Form.Item label="Тип упаковки" name="packing_type"><Input /></Form.Item></Col>
            <Col xs={24} md={24}>
              <Form.Item label="Список контейнеров">
                <Space.Compact style={{ width: '100%' }} direction="vertical">
                  <Form.Item name="containers_list" noStyle>
                    <Input.TextArea rows={3} placeholder="Введите номера контейнеров вручную" />
                  </Form.Item>
                  <Tooltip title="Структура акта уточняется — функция будет доступна позже">
                    <Button icon={<UploadOutlined />} disabled style={{ marginTop: 8 }}>
                      Загрузить из акта
                    </Button>
                  </Tooltip>
                </Space.Compact>
              </Form.Item>
            </Col>
          </Row>
        </Card>

        {/* ── МЕСТО ДОСМОТРА ── */}
        <Card title="Место досмотра" style={{ marginBottom: 16 }}>
          <Row gutter={16}>
            <Col xs={24} md={12}>
              <Form.Item label="Терминал" name="inspection_place">
                <Select
                  showSearch
                  placeholder="Выберите терминал"
                  allowClear
                  filterOption={(input, option) =>
                    (option?.label as string)?.toLowerCase().includes(input.toLowerCase())
                  }
                  options={inspectionPlaces.map((x) => ({ value: x.id, label: x.name }))}
                />
              </Form.Item>
            </Col>
            <Col xs={24} md={12}>
              <Form.Item label="Адрес" name="inspection_place_custom">
                <Input />
              </Form.Item>
            </Col>
          </Row>
        </Card>

        {/* ── МЕЖДУНАРОДНЫЕ СЕРТИФИКАТЫ ── */}
        <Card title="Международные сертификаты" style={{ marginBottom: 16 }}>
          <Form.Item name="documents_needed">
            <Checkbox.Group>
              <Row gutter={[8, 12]}>
                {CERTIFICATE_OPTIONS.map((opt) => (
                  <Col xs={24} sm={12} key={opt.value}>
                    <Checkbox value={opt.value}>{opt.label}</Checkbox>
                  </Col>
                ))}
              </Row>
            </Checkbox.Group>
          </Form.Item>
        </Card>

        {/* ── ДОПОЛНИТЕЛЬНО ── */}
        <Card title="Дополнительно" style={{ marginBottom: 16 }}>
          <Row gutter={16}>
            <Col xs={24} md={12}><Form.Item label="Контактный телефон" name="contact_phone"><Input /></Form.Item></Col>
            <Col xs={24} md={12}><Form.Item label="Контактный email" name="contact_email"><Input type="email" /></Form.Item></Col>
            <Col xs={24}><Form.Item label="Примечания" name="notes"><Input.TextArea rows={3} /></Form.Item></Col>
          </Row>
        </Card>

        {/* ── СГЕНЕРИРОВАННЫЕ ФАЙЛЫ ── */}
        {files.length > 0 && (
          <Card title="Сгенерированные документы">
            <Space wrap>
              {files.map((f) => (
                <Button
                  key={f.id}
                  onClick={() => downloadFile(f)}
                  icon={f.file_name.endsWith('.docx') ? <FileWordOutlined /> : <FileExcelOutlined />}
                >
                  {f.file_name}
                </Button>
              ))}
            </Space>
          </Card>
        )}
      </Form>
    </>
  )
}
