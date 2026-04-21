import { useEffect, useRef, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import {
  Button, Card, Checkbox, Col, DatePicker, Form, Input, InputNumber,
  message, Row, Select, Space, Spin, Tag, Tooltip, Typography,
} from 'antd'
import {
  SaveOutlined, ArrowLeftOutlined, FileWordOutlined,
  FileExcelOutlined, UploadOutlined, PrinterOutlined,
} from '@ant-design/icons'
import dayjs from 'dayjs'
import { applicationsApi } from '../../api/applications'
import { counterpartiesApi, productsApi, terminalsApi, powersOfAttorneyApi } from '../../api/reference'
import type { Counterparty, Product, Terminal, PowerOfAttorney } from '../../types/reference'
import type { Application, GeneratedFile } from '../../types/application'

const CERTIFICATE_OPTIONS = [
  { label: 'Сертификат безопасности и качества', value: 'safety_quality' },
  { label: 'Сертификат здоровья', value: 'health' },
  { label: 'Международный сертификат качества', value: 'intl_quality' },
  { label: 'Радиологический сертификат', value: 'radio' },
  { label: 'Сертификат ГМО', value: 'gmo' },
]

const STATUS_MAP: Record<string, { label: string; color: string }> = {
  draft: { label: 'Черновик', color: 'default' },
  filled: { label: 'Заполнено', color: 'blue' },
  ready_to_print: { label: 'Готово к печати', color: 'green' },
  completed: { label: 'Завершена', color: 'success' },
  archived: { label: 'Архив', color: 'orange' },
}

export default function ApplicationFormPage() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const [form] = Form.useForm()
  const isNew = !id || id === 'new'
  const [loading, setLoading] = useState(!isNew)
  const [saving, setSaving] = useState(false)
  const [generating, setGenerating] = useState(false)
  const [files, setFiles] = useState<GeneratedFile[]>([])
  const [lastSaved, setLastSaved] = useState<Date | null>(null)

  const [applicants, setApplicants] = useState<Counterparty[]>([])
  const [products, setProducts] = useState<Product[]>([])
  const [importers, setImporters] = useState<Counterparty[]>([])
  const [inspectionPlaces, setInspectionPlaces] = useState<Terminal[]>([])
  const [powersOfAttorney, setPowersOfAttorney] = useState<PowerOfAttorney[]>([])

  const [appNumber, setAppNumber] = useState('')
  const [status, setStatus] = useState('draft')

  const autoSaveTimer = useRef<ReturnType<typeof setTimeout> | null>(null)
  const byInstruction = Form.useWatch('by_instruction', form)

  useEffect(() => {
    Promise.all([
      counterpartiesApi.list(),
      productsApi.list(),
      terminalsApi.list(),
      powersOfAttorneyApi.list({ is_active: 'true' }),
    ]).then(([a, p, ip, poa]) => {
      setApplicants(a.data)
      setImporters(a.data)
      setProducts(p.data)
      setInspectionPlaces(ip.data)
      setPowersOfAttorney(poa.data)
    })

    if (!isNew) {
      applicationsApi.get(id!).then(({ data }) => {
        form.setFieldsValue({
          ...data,
          planned_inspection_date: data.planned_inspection_date ? dayjs(data.planned_inspection_date) : null,
        })
        setAppNumber(data.application_number)
        setStatus(data.status ?? 'draft')
        return applicationsApi.getFiles(id!)
      }).then(({ data }) => setFiles(data))
        .finally(() => setLoading(false))
    }

    return () => {
      if (autoSaveTimer.current) clearTimeout(autoSaveTimer.current)
    }
  }, [id])

  const scheduleAutoSave = () => {
    if (isNew || status !== 'draft') return
    if (autoSaveTimer.current) clearTimeout(autoSaveTimer.current)
    autoSaveTimer.current = setTimeout(async () => {
      try {
        await applicationsApi.update(id!, form.getFieldsValue())
        setLastSaved(new Date())
      } catch { /* silent autosave */ }
    }, 2000)
  }

  const fillExporterFields = (a: Counterparty) => {
    form.setFieldsValue({
      exporter_rus: a.name_ru,
      exporter_eng: a.name_en,
      exporter_address: a.legal_address_ru,
      exporter_inn: a.inn,
      exporter_kpp: a.kpp,
      exporter_ogrn: a.ogrn,
    })
  }

  const onApplicantChange = (val: string) => {
    const a = applicants.find((x) => x.uuid === val)
    if (a) fillExporterFields(a)
  }

  const onExporterSelectChange = (val: string) => {
    const a = applicants.find((x) => x.uuid === val)
    if (a) fillExporterFields(a)
  }

  const onProductChange = (val: string) => {
    const p = products.find((x) => x.uuid === val)
    if (p) {
      form.setFieldsValue({
        product_rus: p.name_ru,
        product_eng: p.name_en,
        botanical_name: p.botanical_name_latin,
        tnved_code: p.hs_code_tnved,
      })
    }
  }

  const onInspectionPlaceChange = (val: string) => {
    const t = inspectionPlaces.find((x) => x.uuid === val)
    if (t) form.setFieldsValue({ inspection_place_custom: t.address_ru })
  }

  const onSave = async () => {
    if (autoSaveTimer.current) clearTimeout(autoSaveTimer.current)
    try {
      const values = await form.validateFields()
      setSaving(true)
      if (isNew) {
        const { data } = await applicationsApi.create(values)
        message.success('Заявка создана')
        navigate(`/applications/${data.id}/edit`)
      } else {
        await applicationsApi.update(id!, values)
        setLastSaved(new Date())
        message.success('Заявка сохранена')
      }
    } catch (e: any) {
      if (e?.errorFields) return
      message.error('Ошибка сохранения')
    } finally {
      setSaving(false)
    }
  }

  const onChangeStatus = async (newStatus: string) => {
    try {
      await applicationsApi.changeStatus(id!, newStatus)
      setStatus(newStatus)
    } catch {
      message.error('Ошибка смены статуса')
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
  const statusInfo = STATUS_MAP[status] ?? { label: status, color: 'default' }

  return (
    <>
      {/* ── ШАПКА ── */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16, flexWrap: 'wrap', gap: 8 }}>
        <Space wrap align="center">
          <Button icon={<ArrowLeftOutlined />} onClick={() => navigate('/applications')} className="no-print" />
          <Typography.Title level={4} style={{ margin: 0 }}>{title}</Typography.Title>
          {status && <Tag color={statusInfo.color}>{statusInfo.label}</Tag>}
          {!isNew && status === 'draft' && (
            <Button size="small" className="no-print" onClick={() => onChangeStatus('filled')}>Заполнено</Button>
          )}
          {!isNew && status === 'filled' && (
            <Button size="small" type="primary" className="no-print" onClick={() => onChangeStatus('ready_to_print')}>Готово к печати</Button>
          )}
          {lastSaved && (
            <Typography.Text type="secondary" style={{ fontSize: 12 }}>
              Сохранено в {dayjs(lastSaved).format('HH:mm')}
            </Typography.Text>
          )}
        </Space>
        <Space wrap className="no-print">
          {!isNew && (
            <>
              <Button icon={<PrinterOutlined />} onClick={() => window.print()}>Предпросмотр</Button>
              <Button icon={<FileWordOutlined />} loading={generating} onClick={() => onGenerate(['cokz'])}>СОКЗ</Button>
              <Button icon={<FileExcelOutlined />} loading={generating} onClick={() => onGenerate(['fito1', 'fito2'])}>ФИТО</Button>
              <Button icon={<FileExcelOutlined />} loading={generating} onClick={() => onGenerate(['act'])}>АКТ</Button>
              <Button onClick={() => onGenerate(['cokz', 'fito1', 'fito2', 'act'])} loading={generating}>Все документы</Button>
            </>
          )}
          <Button type="primary" icon={<SaveOutlined />} loading={saving} onClick={onSave}>Сохранить</Button>
        </Space>
      </div>

      <Form form={form} layout="vertical" size="middle" onValuesChange={scheduleAutoSave}>

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
                  options={applicants.map((a) => ({ value: a.uuid, label: `${a.name_ru} (ИНН: ${a.inn ?? '—'})` }))}
                />
              </Form.Item>
            </Col>
            <Col xs={24} md={12}>
              <Form.Item label="Юридический адрес компании Заявитель" name="applicant_custom">
                <Input />
              </Form.Item>
            </Col>
            <Col xs={24} md={12}>
              <Form.Item label="Фактический адрес компании Заявитель" name="applicant_actual_address">
                <Input />
              </Form.Item>
            </Col>
            <Col xs={24} md={12}>
              <Form.Item label="Контактная информация" name="poruchenie">
                <Input />
              </Form.Item>
            </Col>
            <Col xs={24} md={12}>
              <Form.Item label="Доверенность №" name="doverennost">
                <Select
                  showSearch
                  placeholder="Выберите доверенность"
                  allowClear
                  filterOption={(input, option) =>
                    (option?.label as string)?.toLowerCase().includes(input.toLowerCase())
                  }
                  options={powersOfAttorney.map((p) => ({ value: p.uuid, label: p.poa_number }))}
                />
              </Form.Item>
            </Col>
            <Col xs={24} md={6}>
              <Form.Item label="№ Договора с ЦОК АПК" name="contract_number_cok">
                <Input />
              </Form.Item>
            </Col>
            <Col xs={24} md={6}>
              <Form.Item label="Дата договора" name="contract_date_cok">
                <DatePicker format="DD.MM.YYYY" style={{ width: '100%' }} placeholder="дд.мм.гггг" />
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
                  options={applicants.map((a) => ({ value: a.uuid, label: `${a.inn ?? '—'} — ${a.name_ru}` }))}
                />
              </Form.Item>
            </Col>
            <Col xs={24} md={12}><Form.Item label="Наименование (рус)" name="exporter_rus"><Input /></Form.Item></Col>
            <Col xs={24} md={12}><Form.Item label="Наименование (eng)" name="exporter_eng"><Input /></Form.Item></Col>
            <Col xs={24} md={24}><Form.Item label="Адрес" name="exporter_address"><Input /></Form.Item></Col>
            <Col xs={24} md={8}><Form.Item label="ИНН" name="exporter_inn"><Input /></Form.Item></Col>
            <Col xs={24} md={8}><Form.Item label="КПП" name="exporter_kpp"><Input /></Form.Item></Col>
            <Col xs={24} md={8}><Form.Item label="ОГРН" name="exporter_ogrn"><Input /></Form.Item></Col>
            <Col xs={24} md={24}>
              <Form.Item name="by_instruction" valuePropName="checked">
                <Checkbox>По поручению</Checkbox>
              </Form.Item>
            </Col>
            {byInstruction && (
              <Col xs={24} md={24}>
                <Form.Item label="Текст поручения" name="instruction_text">
                  <Input.TextArea rows={2} />
                </Form.Item>
              </Col>
            )}
            <Col xs={24} md={24}>
              <Form.Item label="Дата и номер контракта/распоряжения на поставку" name="supply_contract_info">
                <Input />
              </Form.Item>
            </Col>
          </Row>
        </Card>

        {/* ── ПОЛУЧАТЕЛЬ ── */}
        <Card title="Получатель" style={{ marginBottom: 16 }}>
          <Row gutter={16}>
            <Col xs={24} md={12}>
              <Form.Item label="Получатель из справочника" name="importer">
                <Select
                  showSearch
                  placeholder="Выберите получателя"
                  allowClear
                  filterOption={(input, option) =>
                    (option?.label as string)?.toLowerCase().includes(input.toLowerCase())
                  }
                  options={importers.map((x) => ({ value: x.uuid, label: x.name_en ?? x.name_ru }))}
                />
              </Form.Item>
            </Col>
            <Col xs={24} md={12}><Form.Item label="Получатель (вручную)" name="importer_custom"><Input /></Form.Item></Col>
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
                  options={products.map((x) => ({ value: x.uuid, label: x.name_ru }))}
                />
              </Form.Item>
            </Col>
            <Col xs={24} md={12}><Form.Item label="Продукция (вручную)" name="product_custom"><Input /></Form.Item></Col>
            <Col xs={24} md={12}><Form.Item label="Наименование (рус)" name="product_rus"><Input /></Form.Item></Col>
            <Col xs={24} md={12}><Form.Item label="Наименование (eng)" name="product_eng"><Input /></Form.Item></Col>
            <Col xs={24} md={12}><Form.Item label="Ботаническое название" name="botanical_name"><Input /></Form.Item></Col>
            <Col xs={24} md={12}><Form.Item label="Код ТНВЭД" name="tnved_code"><Input /></Form.Item></Col>
            <Col xs={24}>
              <Form.Item label="Исследования будут произведены на соответствие документам:" name="research_docs">
                <Input.TextArea rows={2} />
              </Form.Item>
            </Col>
          </Row>
        </Card>

        {/* ── ГРУЗ ── */}
        <Card title="Груз и отгрузка" style={{ marginBottom: 16 }}>
          <Row gutter={16}>
            <Col xs={24} md={8}>
              <Form.Item label="Вес (тонн)" name="weight_tons">
                <InputNumber style={{ width: '100%' }} step={0.001} decimalSeparator="," />
              </Form.Item>
            </Col>
            <Col xs={24} md={8}>
              <Form.Item label="Количество мест" name="places_count">
                <Input placeholder="Например: 24 или навал" />
              </Form.Item>
            </Col>
            <Col xs={24} md={8}>
              <Form.Item label="Тип упаковки" name="packing_type">
                <Input />
              </Form.Item>
            </Col>
            <Col xs={24} md={12}>
              <Form.Item label="Пункт назначения" name="destination_place">
                <Input placeholder="HUANGPU, CHINA / ХУАНГПУ, КИТАЙ" />
              </Form.Item>
            </Col>
            <Col xs={24} md={24}>
              <Form.Item label="Список контейнеров" name="containers_list">
                <Input.TextArea rows={3} placeholder="Введите номера контейнеров вручную" />
              </Form.Item>
              <Tooltip title="Структура акта уточняется — функция будет доступна позже">
                <Button icon={<UploadOutlined />} disabled style={{ marginBottom: 16 }}>
                  Загрузить из акта
                </Button>
              </Tooltip>
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
                  onChange={onInspectionPlaceChange}
                  options={inspectionPlaces.map((x) => ({ value: x.uuid, label: x.terminal_name }))}
                />
              </Form.Item>
            </Col>
            <Col xs={24} md={12}>
              <Form.Item label="Адрес" name="inspection_place_custom">
                <Input />
              </Form.Item>
            </Col>
            <Col xs={24} md={12}>
              <Form.Item label="Предполагаемая дата начала инспекции" name="planned_inspection_date">
                <DatePicker format="DD.MM.YYYY" style={{ width: '100%' }} placeholder="дд.мм.гггг" />
              </Form.Item>
            </Col>
          </Row>
        </Card>

        {/* ── МЕЖДУНАРОДНЫЕ СЕРТИФИКАТЫ ── */}
        <Card title="Международные сертификаты" style={{ marginBottom: 16 }}>
          {CERTIFICATE_OPTIONS.map((opt) => (
            <Row key={opt.value} align="middle" gutter={8} style={{ marginBottom: 10 }}>
              <Col flex="auto">
                <Form.Item name={`cert_${opt.value}_checked`} valuePropName="checked" noStyle>
                  <Checkbox>{opt.label}</Checkbox>
                </Form.Item>
              </Col>
              <Col>
                <Space>
                  <Typography.Text type="secondary" style={{ fontSize: 13 }}>Копий:</Typography.Text>
                  <Form.Item noStyle dependencies={[`cert_${opt.value}_checked`]}>
                    {({ getFieldValue }) => (
                      <Form.Item name={`cert_${opt.value}_copies`} noStyle>
                        <InputNumber
                          min={0}
                          disabled={!getFieldValue(`cert_${opt.value}_checked`)}
                          style={{ width: 70 }}
                        />
                      </Form.Item>
                    )}
                  </Form.Item>
                </Space>
              </Col>
            </Row>
          ))}
        </Card>

        {/* ── ДОПОЛНИТЕЛЬНО ── */}
        <Card title="Дополнительно" style={{ marginBottom: 16 }}>
          <Row gutter={16}>
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
