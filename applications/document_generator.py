# applications/document_generator.py

import os
import datetime
from docx import Document
from docx.shared import Inches, Pt
from openpyxl import load_workbook
from openpyxl.styles import Font, Alignment
from django.conf import settings
import tempfile

class DocumentGenerator:
    """Класс для генерации документов по шаблонам"""
    
    def __init__(self):
        self.templates_dir = settings.TEMPLATES_DIR
        
    def generate_all(self, application):
        """Генерирует все документы для заявки"""
        files = []
        
        # Определяем, какие документы нужны
        docs_needed = application.documents_needed or {}
        
        # Всегда генерируем заявку в ЦОКЗ
        cokz_file = self.generate_cokz(application)
        if cokz_file:
            files.append(cokz_file)
        
        # Генерируем фито-документы, если нужно
        if docs_needed.get('fito', False) or True:  # Временно всегда генерируем
            fito_files = self.generate_fito(application)
            files.extend(fito_files)
        
        return files
    
    def generate_cokz(self, application):
        """Генерация заявки в ЦОК АПК (Word)"""
        template_path = os.path.join(self.templates_dir, 'cokz_template.docx')
        
        # Если шаблона нет, создаем временный документ с данными
        if not os.path.exists(template_path):
            doc = Document()
            doc.add_heading('ЗАЯВКА', 0)
            doc.add_paragraph(f'Наименование заявителя: {application.applicant.name_rus if application.applicant else application.applicant_custom}')
            doc.add_paragraph(f'ИНН/КПП: {application.applicant.inn if application.applicant else ""}')
            doc.add_paragraph(f'Продукция: {application.product.name_rus if application.product else application.product_rus}')
            doc.add_paragraph(f'Вес: {application.weight_tons} тонн')
            doc.add_paragraph(f'Контейнеры: {application.containers_list}')
        else:
            doc = Document(template_path)
            # Здесь будет логика замены меток в шаблоне
            # Например: {{ЗАЯВИТЕЛЬ}} -> application.applicant.name_rus
        
        # Сохраняем во временный файл
        temp_file = tempfile.NamedTemporaryFile(
            suffix='.docx', 
            dir=os.path.join(settings.MEDIA_ROOT, 'temp'),
            delete=False
        )
        doc.save(temp_file.name)
        
        # Создаем постоянный файл
        filename = f"cokz_{application.application_number}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.docx"
        final_path = os.path.join(settings.MEDIA_ROOT, 'generated_docs', 
                                  application.created_at.strftime('%Y/%m/%d'), filename)
        
        os.makedirs(os.path.dirname(final_path), exist_ok=True)
        os.rename(temp_file.name, final_path)
        
        return {
            'name': filename,
            'path': final_path,
            'type': 'cokz'
        }
    
    def generate_fito(self, application):
        """Генерация фитосанитарных документов (Excel)"""
        files = []
        
        # Создаем временную директорию
        temp_dir = tempfile.mkdtemp()
        
        # Генерируем лист 1 (Заявление на выдачу фитосертификата)
        wb = load_workbook(os.path.join(self.templates_dir, 'fito_template.xlsx')) if os.path.exists(os.path.join(self.templates_dir, 'fito_template.xlsx')) else None
        
        if not wb:
            # Создаем простой Excel с данными
            from openpyxl import Workbook
            wb = Workbook()
            ws = wb.active
            ws.title = "Фито (1)"
            
            # Заполняем данными
            data = [
                ['OOO «Блэк Си Групп-Логистик»', '', '', 'ИНН', application.applicant.inn if application.applicant else ''],
                ['Краснодарский край', '', '', 'КПП', application.applicant.kpp if application.applicant else ''],
                ['', '', '', 'ОГРН', application.applicant.ogrn if application.applicant else ''],
                [],
                ['Заявление на выдачу фитосанитарного сертификата'],
                [],
                ['Экспортер продукции и его адрес:'],
                [application.exporter_rus],
                [''],
                ['ИНН:', application.exporter_inn],
                ['Получатель продукции и его адрес:'],
                [application.importer.name_eng if application.importer else application.importer_name_eng],
                [application.importer.address_eng if application.importer else application.importer_address_eng],
                [],
                ['Наименование продукции и ее количество:', application.product.name_rus if application.product else application.product_rus, f"{application.weight_mt} MT"],
                ['Ботаническое название:', application.botanical_name],
                ['Количество мест и описание упаковки:', application.packing_type],
                ['Отличительные знаки:', 'NONE'],
                ['Место происхождения груза:', application.origin_country],
                ['Способ транспортировки:', f"BY SEA/CONTAINER {application.containers_list[:100]}..."],
                ['Пункт ввоза или страна назначения:', application.importer_city],
                ['Представитель получателя груза:', 'Козюпа С.В.'],
                ['Контактный телефон:', application.contact_phone],
                ['Email:', application.contact_email]
            ]
            
            for row_idx, row_data in enumerate(data, 1):
                for col_idx, value in enumerate(row_data, 1):
                    cell = ws.cell(row=row_idx, column=col_idx, value=value)
        
        # Сохраняем лист 1
        filename1 = f"fito1_{application.application_number}.xlsx"
        path1 = os.path.join(settings.MEDIA_ROOT, 'generated_docs', 
                             application.created_at.strftime('%Y/%m/%d'), filename1)
        os.makedirs(os.path.dirname(path1), exist_ok=True)
        wb.save(path1)
        
        files.append({
            'name': filename1,
            'path': path1,
            'type': 'fito1'
        })
        
        # Генерируем лист 2 (Заявление на отбор проб)
        wb2 = Workbook()
        ws2 = wb2.active
        ws2.title = "Фито (2)"
        
        # Копируем данные из первого листа, но с другим форматом
        ws2['A1'] = 'Заявление на отбор проб и установление карантинного фитосанитарного состояния'
        ws2['A3'] = f"Экспортер: {application.exporter_rus}"
        ws2['A4'] = f"ИНН: {application.exporter_inn}"
        ws2['A5'] = f"Получатель: {application.importer.name_eng if application.importer else application.importer_name_eng}"
        ws2['A6'] = f"Продукция: {application.product.name_rus if application.product else application.product_rus}"
        ws2['A7'] = f"Количество: {application.weight_mt} MT"
        ws2['A8'] = f"Место отбора: {application.inspection_place.name if application.inspection_place else application.inspection_place_custom}"
        
        filename2 = f"fito2_{application.application_number}.xlsx"
        path2 = os.path.join(settings.MEDIA_ROOT, 'generated_docs', 
                             application.created_at.strftime('%Y/%m/%d'), filename2)
        wb2.save(path2)
        
        files.append({
            'name': filename2,
            'path': path2,
            'type': 'fito2'
        })
        
        # Генерируем акт досмотра
        wb3 = Workbook()
        ws3 = wb3.active
        ws3.title = "Акт досмотра"
        
        ws3['A1'] = 'АКТ ДОСМОТРА ПОДКАРАНТИННЫХ МАТЕРИАЛОВ'
        ws3['A3'] = f"Наименование продукции: {application.product.name_rus if application.product else application.product_rus}"
        ws3['A4'] = f"Транспортное средство: {application.containers_list[:100]}"
        ws3['A5'] = f"Экспортер: {application.exporter_rus}"
        ws3['A6'] = f"Импортер: {application.importer.name_eng if application.importer else application.importer_name_eng}"
        ws3['A7'] = f"Количество: {application.weight_tons} тонн, {application.places_count}"
        ws3['A8'] = f"Место отбора: {application.inspection_place.name if application.inspection_place else application.inspection_place_custom}"
        
        filename3 = f"act_{application.application_number}.xlsx"
        path3 = os.path.join(settings.MEDIA_ROOT, 'generated_docs', 
                             application.created_at.strftime('%Y/%m/%d'), filename3)
        wb3.save(path3)
        
        files.append({
            'name': filename3,
            'path': path3,
            'type': 'act'
        })
        
        return files