import uuid as _uuid_module
from dataclasses import dataclass
from decimal import Decimal
from typing import Optional

from django.db import transaction
from rest_framework.exceptions import ValidationError

from .models import Application
from .selectors import ApplicationDocumentResolver
from reference.models import LookupStatusCode, Terminal, Product, PowerOfAttorney
from accounts.models import Counterparty, Account


@dataclass
class StuffingActAggregate:
    weight_mt: Optional[Decimal] = None
    container_count: Optional[int] = None
    containers_text: Optional[str] = None
    places_value: Optional[str] = None
    transport_text: Optional[str] = None


class StuffingActService:
    """
    Адаптер над уже существующей логикой акта затарки.

    Сейчас здесь заглушка по контракту.
    Когда покажешь реальный код/модель акта затарки, сюда просто
    подключим фактический запрос в БД.
    """

    def get_aggregate(self, stuffing_act_uuid) -> StuffingActAggregate:
        if not stuffing_act_uuid:
            return StuffingActAggregate()

        # TODO: заменить на реальную реализацию
        # act = StuffingAct.objects.get(uuid=stuffing_act_uuid)
        # items = StuffingActItem.objects.filter(act=act)
        return StuffingActAggregate()


class ApplicationService:
    def __init__(
        self,
        stuffing_act_service: Optional[StuffingActService] = None,
        document_resolver: Optional[ApplicationDocumentResolver] = None,
    ):
        self.stuffing_act_service = stuffing_act_service or StuffingActService()
        self.document_resolver = document_resolver or ApplicationDocumentResolver()

    def get_queryset(self):
        return (
            Application.objects
            .select_related(
                'status',
                'applicant_counterparty',
                'applicant_account',
                'terminal',
                'product',
                'power_of_attorney',
                'master_application',
            )
            .all()
        )

    def get_by_uuid(self, application_uuid):
        return self.get_queryset().get(uuid=application_uuid)

    @transaction.atomic
    def create(self, validated_data: dict) -> Application:
        self._validate_business_rules(validated_data, is_update=False)

        fields = {
            'application_number': validated_data.get('application_number'),
            'application_type_code': validated_data.get(
                'application_type_code', Application.TYPE_VNIIKR,
            ),
            'applicant_counterparty': self._resolve_counterparty(
                validated_data.get('applicant_counterparty_uuid')
            ),
            'applicant_account': self._resolve_account(
                validated_data.get('applicant_account_uuid')
            ),
            'terminal': self._resolve_terminal(validated_data.get('terminal_uuid')),
            'product': self._resolve_product(validated_data.get('product_uuid')),
            'power_of_attorney': self._resolve_power_of_attorney(
                validated_data.get('power_of_attorney_uuid')
            ),
            'status': self._resolve_status(validated_data.get('status_code') or 'draft'),
            'master_application': self._resolve_master_application(
                validated_data.get('master_application_uuid')
            ),
            'stuffing_act_uuid': validated_data.get('stuffing_act_uuid'),
            'sender_en_manual': validated_data.get('sender_en_manual'),
            'product_name_en_manual': validated_data.get('product_name_en_manual'),
            'contract_number_manual': validated_data.get('contract_number_manual'),
            'contract_date_manual': validated_data.get('contract_date_manual'),
            'discharge_port_ru_manual': validated_data.get('discharge_port_ru_manual'),
            'discharge_port_en_manual': validated_data.get('discharge_port_en_manual'),
            'additional_declaration': validated_data.get('additional_declaration'),
            'notes': validated_data.get('notes'),
            'harvest_year': validated_data.get('harvest_year'),
            'manufacture_date': validated_data.get('manufacture_date'),
            'weight_mt': validated_data.get('weight_mt'),
            'planned_inspection_date': validated_data.get('planned_inspection_date'),
            'planned_inspection_time': validated_data.get('planned_inspection_time'),
            'ikr_number': validated_data.get('ikr_number'),
            'ikr_date': validated_data.get('ikr_date'),
            'asid_number': validated_data.get('asid_number'),
            'is_on_behalf': validated_data.get('is_on_behalf', False),
            'need_color_letter': validated_data.get('need_color_letter', False),
            'is_active': validated_data.get('is_active', True),
        }

        # Stuffing snapshot ДО create — один INSERT, без повторного save
        stuffing_act_uuid = validated_data.get('stuffing_act_uuid')
        if stuffing_act_uuid:
            aggregate = self.stuffing_act_service.get_aggregate(stuffing_act_uuid)
            if aggregate.weight_mt is not None:
                fields['weight_mt'] = aggregate.weight_mt

        return Application.objects.create(**fields)

    @transaction.atomic
    def update(self, application: Application, validated_data: dict) -> Application:
        self._validate_business_rules(validated_data, is_update=True, instance=application)

        if 'application_number' in validated_data:
            application.application_number = validated_data.get('application_number')

        if 'application_type_code' in validated_data:
            application.application_type_code = validated_data.get('application_type_code')

        if 'applicant_counterparty_uuid' in validated_data:
            application.applicant_counterparty = self._resolve_counterparty(
                validated_data.get('applicant_counterparty_uuid')
            )

        if 'applicant_account_uuid' in validated_data:
            application.applicant_account = self._resolve_account(
                validated_data.get('applicant_account_uuid')
            )

        if 'terminal_uuid' in validated_data:
            application.terminal = self._resolve_terminal(
                validated_data.get('terminal_uuid')
            )

        if 'product_uuid' in validated_data:
            application.product = self._resolve_product(
                validated_data.get('product_uuid')
            )

        if 'power_of_attorney_uuid' in validated_data:
            application.power_of_attorney = self._resolve_power_of_attorney(
                validated_data.get('power_of_attorney_uuid')
            )

        if 'status_code' in validated_data:
            application.status = self._resolve_status(validated_data.get('status_code'))

        if 'master_application_uuid' in validated_data:
            application.master_application = self._resolve_master_application(
                validated_data.get('master_application_uuid')
            )

        scalar_fields = [
            'stuffing_act_uuid',
            'sender_en_manual',
            'product_name_en_manual',
            'contract_number_manual',
            'contract_date_manual',
            'discharge_port_ru_manual',
            'discharge_port_en_manual',
            'additional_declaration',
            'notes',
            'harvest_year',
            'manufacture_date',
            'weight_mt',
            'planned_inspection_date',
            'planned_inspection_time',
            'ikr_number',
            'ikr_date',
            'asid_number',
            'is_on_behalf',
            'need_color_letter',
            'is_active',
        ]

        for field in scalar_fields:
            if field in validated_data:
                setattr(application, field, validated_data.get(field))

        application.save()

        if 'stuffing_act_uuid' in validated_data:
            self._apply_stuffing_snapshot_if_needed(application)

        return application

    def get_available_documents(self, application: Application) -> list[str]:
        return self.document_resolver.resolve(application)

    def preview(self, application: Application) -> dict:
        return {
            'uuid': str(application.uuid),
            'application_number': application.application_number,
            'application_type_code': application.application_type_code,
            'status_code': application.status_id,
            'weight_mt': application.weight_mt,
            'documents': self.get_available_documents(application),
            'has_master': bool(application.master_application_id),
            'stuffing_act_uuid': str(application.stuffing_act_uuid) if application.stuffing_act_uuid else None,
        }

    def _apply_stuffing_snapshot_if_needed(self, application: Application):
        if not application.stuffing_act_uuid:
            return

        aggregate = self.stuffing_act_service.get_aggregate(application.stuffing_act_uuid)

        update_fields = []

        if aggregate.weight_mt is not None:
            application.weight_mt = aggregate.weight_mt
            update_fields.append('weight_mt')

        if update_fields:
            application.save(update_fields=update_fields + ['updated_at'])

    def _resolve_status(self, status_code: Optional[str]):
        if not status_code:
            return None
        try:
            return LookupStatusCode.objects.get(status_code=status_code)
        except LookupStatusCode.DoesNotExist:
            raise ValidationError({'status_code': 'Указан несуществующий статус.'})

    def _resolve_terminal(self, terminal_uuid):
        if not terminal_uuid:
            return None
        try:
            return Terminal.objects.get(uuid=terminal_uuid)
        except Terminal.DoesNotExist:
            raise ValidationError({'terminal_uuid': 'Указан несуществующий terminal_uuid.'})

    def _resolve_product(self, product_uuid):
        if not product_uuid:
            return None
        try:
            return Product.objects.get(uuid=product_uuid)
        except Product.DoesNotExist:
            raise ValidationError({'product_uuid': 'Указан несуществующий product_uuid.'})

    def _resolve_power_of_attorney(self, poa_uuid):
        if not poa_uuid:
            return None
        try:
            return PowerOfAttorney.objects.get(uuid=poa_uuid)
        except PowerOfAttorney.DoesNotExist:
            raise ValidationError({'power_of_attorney_uuid': 'Указан несуществующий power_of_attorney_uuid.'})

    def _resolve_counterparty(self, counterparty_uuid):
        if not counterparty_uuid:
            return None
        try:
            return Counterparty.objects.get(uuid=counterparty_uuid)
        except Counterparty.DoesNotExist:
            raise ValidationError({'applicant_counterparty_uuid': 'Указан несуществующий applicant_counterparty_uuid.'})

    def _resolve_account(self, account_uuid):
        if not account_uuid:
            return None
        try:
            return Account.objects.get(uuid=account_uuid)
        except Account.DoesNotExist:
            raise ValidationError({'applicant_account_uuid': 'Указан несуществующий applicant_account_uuid.'})

    def _resolve_master_application(self, application_uuid):
        if not application_uuid:
            return None
        try:
            return Application.objects.get(uuid=application_uuid)
        except Application.DoesNotExist:
            raise ValidationError({'master_application_uuid': 'Указана несуществующая master_application_uuid.'})

    def _validate_business_rules(self, data: dict, is_update: bool, instance: Optional[Application] = None):
        application_type_code = data.get(
            'application_type_code',
            instance.application_type_code if instance else Application.TYPE_VNIIKR
        )
        master_application_uuid = data.get(
            'master_application_uuid',
            instance.master_application_id if instance else None
        )
        ikr_number = data.get('ikr_number', getattr(instance, 'ikr_number', None) if instance else None)
        ikr_date = data.get('ikr_date', getattr(instance, 'ikr_date', None) if instance else None)
        asid_number = data.get('asid_number', getattr(instance, 'asid_number', None) if instance else None)

        if ikr_number and not ikr_date:
            raise ValidationError({'ikr_date': 'Если указан ИКР, нужно указать дату ИКР.'})

        if ikr_number and asid_number:
            raise ValidationError({'non_field_errors': 'Нельзя одновременно указывать ИКР и ASID.'})

        if application_type_code != Application.TYPE_COK_SPLIT and master_application_uuid:
            raise ValidationError({
                'master_application_uuid': 'Связь с master_application допустима только для типа cok_split.'
            })

        if instance and master_application_uuid:
            try:
                normalized_master_uuid = _uuid_module.UUID(str(master_application_uuid))
            except (ValueError, AttributeError):
                raise ValidationError({
                    'master_application_uuid': 'Невалидный UUID формат.'
                })
            if instance.uuid == normalized_master_uuid:
                raise ValidationError({
                    'master_application_uuid': 'Заявка не может ссылаться сама на себя как на master.'
                })


class MasterApplicationService:
    """
    Пока минимальная версия, без дочерних таблиц контейнеров/разбивки.
    Работает только через self-FK master_application_uuid.
    """

    @transaction.atomic
    def bind_children(self, master_application: Application, child_applications: list[Application]):
        if master_application.application_type_code != Application.TYPE_COK_SPLIT:
            raise ValidationError({'non_field_errors': 'Master-заявка должна иметь тип cok_split.'})

        for child in child_applications:
            if child.uuid == master_application.uuid:
                raise ValidationError({'non_field_errors': 'Нельзя привязать заявку саму к себе.'})
            child.master_application = master_application
            child.save(update_fields=['master_application', 'updated_at'])

    @transaction.atomic
    def unbind_child(self, child_application: Application):
        child_application.master_application = None
        child_application.save(update_fields=['master_application', 'updated_at'])
