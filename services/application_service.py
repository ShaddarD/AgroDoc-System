from django.db import transaction
from django.core.exceptions import ValidationError
from .models import Application


class ApplicationService:

    @transaction.atomic
    def create(self, data, actor):

        self._validate(data)

        application = Application.objects.create(
            application_number=data['application_number'],
            application_type_code=data['application_type_code'],

            terminal_id=data['terminal_uuid'],
            product_id=data['product_uuid'],

            sender_en_manual=data['sender_en_manual'],
            product_name_en_manual=data['product_name_en_manual'],

            contract_number_manual=data['contract_number_manual'],
            contract_date_manual=data['contract_date_manual'],

            discharge_port_ru_manual=data['discharge_port_ru_manual'],
            discharge_port_en_manual=data['discharge_port_en_manual'],

            planned_inspection_date=data['planned_inspection_date'],
            planned_inspection_time=data.get('planned_inspection_time'),

            stuffing_act_uuid=data.get('stuffing_act_uuid'),

            ikr_number=data.get('ikr_number'),
            ikr_date=data.get('ikr_date'),
            asid_number=data.get('asid_number'),

            is_on_behalf=data.get('is_on_behalf', False),
            need_color_letter=data.get('need_color_letter', False),
        )

        # 🔥 подтянуть данные из акта
        if application.stuffing_act_uuid:
            self._apply_stuffing_data(application)

        return application

    def _apply_stuffing_data(self, application):
        # тут ты подключаешь уже существующий код
        # который у тебя импортирует Excel
        data = get_stuffing_aggregate(application.stuffing_act_uuid)

        application.weight_mt = data['weight']
        application.save()

    def _validate(self, data):

        if data.get('ikr_number') and not data.get('ikr_date'):
            raise ValidationError('ИКР требует дату')

        if data.get('asid_number') and data.get('ikr_number'):
            raise ValidationError('Нельзя одновременно ASID и ИКР')