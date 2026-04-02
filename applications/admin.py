from django.contrib import admin
from .models import (
    Application, ApplicationContainer, ApplicationCertificate,
    ApplicationRegulation, GeneratedFile, ApplicationHistory, InspectionRecord,
)


class ApplicationContainerInline(admin.TabularInline):
    model = ApplicationContainer
    extra = 0
    fields = ('container_number', 'sort_order')


class ApplicationCertificateInline(admin.TabularInline):
    model = ApplicationCertificate
    extra = 0
    fields = ('certificate', 'copies_count', 'is_required')


class ApplicationRegulationInline(admin.TabularInline):
    model = ApplicationRegulation
    extra = 0
    fields = ('regulation', 'comment')


class GeneratedFileInline(admin.TabularInline):
    model = GeneratedFile
    extra = 0
    fields = ('file_name', 'file_type', 'file_path', 'created_by', 'created_at')
    readonly_fields = ('file_name', 'file_type', 'file_path', 'created_by', 'created_at')
    can_delete = True

    def has_add_permission(self, request, obj=None):
        return False


class ApplicationHistoryInline(admin.TabularInline):
    model = ApplicationHistory
    extra = 0
    fields = ('created_at', 'user', 'action', 'changes')
    readonly_fields = ('created_at', 'user', 'action', 'changes')
    can_delete = False
    ordering = ('-created_at',)

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = (
        'application_number', 'status', 'sender_ru', 'receiver',
        'product', 'weight_mt', 'planned_inspection_date', 'created_by', 'created_at',
    )
    list_filter = ('status', 'created_at', 'planned_inspection_date')
    search_fields = (
        'application_number', 'product__name_ru', 'receiver__name_en',
        'sender_ru__name', 'containers__container_number',
    )
    readonly_fields = ('application_number', 'created_at', 'updated_at')
    date_hierarchy = 'created_at'
    save_on_top = True
    inlines = [
        ApplicationContainerInline, ApplicationCertificateInline,
        ApplicationRegulationInline, GeneratedFileInline, ApplicationHistoryInline,
    ]
    fieldsets = (
        ('Основная информация', {
            'fields': ('application_number', 'status', 'created_by', 'created_at', 'updated_at'),
        }),
        ('Отправитель', {
            'fields': ('sender_ru', 'sender_power_of_attorney', 'sender_en_manual'),
        }),
        ('Получатель', {
            'fields': ('receiver',),
        }),
        ('Продукция', {
            'fields': (
                'product', 'product_name_en_manual', 'harvest_year',
                'manufacture_date', 'purpose',
            ),
        }),
        ('Отгрузка', {
            'fields': (
                'weight_mt', 'packing_type', 'import_country',
                'discharge_port_ru_manual', 'discharge_port_en_manual',
            ),
        }),
        ('Представитель и лаборатория', {
            'fields': (
                'representative', 'sampling_place', 'laboratory',
                'contract_number_manual', 'contract_date_manual',
                'planned_inspection_date', 'additional_declaration',
            ),
        }),
    )


@admin.register(GeneratedFile)
class GeneratedFileAdmin(admin.ModelAdmin):
    list_display = ('file_name', 'file_type', 'application', 'created_by', 'created_at')
    list_filter = ('file_type', 'created_at')
    search_fields = ('file_name', 'application__application_number')
    readonly_fields = ('created_at',)


@admin.register(ApplicationHistory)
class ApplicationHistoryAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'application', 'user', 'action')
    list_filter = ('created_at', 'user')
    search_fields = ('action', 'application__application_number', 'user__username')
    readonly_fields = ('application', 'user', 'action', 'changes', 'created_at')
    date_hierarchy = 'created_at'

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(InspectionRecord)
class InspectionRecordAdmin(admin.ModelAdmin):
    list_display = (
        'number', 'client', 'manager', 'commodity', 'container_count',
        'pod', 'inspection_date_plan', 'fss_date_plan', 'cargo_status', 'documents_status',
    )
    list_filter = ('cargo_status', 'documents_status', 'quarantine', 'inspection_date_plan')
    search_fields = ('number', 'client', 'manager', 'commodity', 'pod', 'terminal', 'comments')
    list_editable = ('cargo_status', 'documents_status')
    date_hierarchy = 'inspection_date_plan'
    ordering = ('inspection_date_plan',)
