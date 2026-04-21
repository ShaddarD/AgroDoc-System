from django.contrib import admin
from .models import Application, InspectionRecord


@admin.register(InspectionRecord)
class InspectionRecordAdmin(admin.ModelAdmin):
    list_display = (
        'number', 'client', 'manager', 'commodity',
        'pod', 'inspection_date_plan', 'fss_date_plan', 'cargo_status', 'documents_status',
    )
    list_filter = ('cargo_status', 'documents_status', 'quarantine', 'inspection_date_plan')
    search_fields = ('number', 'client', 'manager', 'commodity', 'pod', 'terminal', 'comments')
    list_editable = ('cargo_status', 'documents_status')
    ordering = ('inspection_date_plan',)
