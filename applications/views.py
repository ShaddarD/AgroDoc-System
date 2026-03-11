# applications/views.py

from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import FileResponse
import os

from .models import Application, GeneratedFile, ApplicationHistory
from .serializers import (
    ApplicationListSerializer, ApplicationDetailSerializer,
    ApplicationCreateSerializer, GeneratedFileSerializer
)
from .document_generator import DocumentGenerator

class ApplicationViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с заявками"""
    
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Фильтрация заявок для текущего пользователя"""
        queryset = Application.objects.all()
        
        # Фильтр по статусу
        status = self.request.query_params.get('status', None)
        if status:
            queryset = queryset.filter(status=status)
        
        # Поиск
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(application_number__icontains=search) |
                Q(product_rus__icontains=search) |
                Q(importer_name_eng__icontains=search) |
                Q(containers_list__icontains=search)
            )
        
        # Фильтр по дате
        date_from = self.request.query_params.get('date_from', None)
        date_to = self.request.query_params.get('date_to', None)
        if date_from:
            queryset = queryset.filter(created_at__date__gte=date_from)
        if date_to:
            queryset = queryset.filter(created_at__date__lte=date_to)
        
        return queryset
    
    def get_serializer_class(self):
        """Выбор сериализатора в зависимости от действия"""
        if self.action == 'list':
            return ApplicationListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return ApplicationCreateSerializer
        return ApplicationDetailSerializer
    
    def perform_create(self, serializer):
        """Сохранение с указанием автора"""
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['post'])
    def generate_documents(self, request, pk=None):
        """Генерация документов для заявки"""
        application = self.get_object()
        
        try:
            generator = DocumentGenerator()
            files = generator.generate_all(application)
            
            # Сохраняем информацию о файлах в БД
            generated_files = []
            for file_info in files:
                file_obj = GeneratedFile.objects.create(
                    application=application,
                    file_name=file_info['name'],
                    file_path=file_info['path'],
                    file_type=file_info['type'],
                    created_by=request.user
                )
                generated_files.append(file_obj)
            
            # Обновляем статус заявки
            application.status = 'completed'
            application.save()
            
            # Записываем в историю
            ApplicationHistory.objects.create(
                application=application,
                user=request.user,
                action='Сгенерированы документы',
                changes={'files': [f.name for f in generated_files]}
            )
            
            serializer = GeneratedFileSerializer(generated_files, many=True)
            return Response(serializer.data)
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['get'])
    def files(self, request, pk=None):
        """Получение списка сгенерированных файлов"""
        application = self.get_object()
        files = application.files.all()
        serializer = GeneratedFileSerializer(files, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def change_status(self, request, pk=None):
        """Изменение статуса заявки"""
        application = self.get_object()
        new_status = request.data.get('status')
        
        if new_status in dict(Application.STATUS_CHOICES):
            old_status = application.status
            application.status = new_status
            application.save()
            
            # Записываем в историю
            ApplicationHistory.objects.create(
                application=application,
                user=request.user,
                action=f'Изменен статус: {old_status} -> {new_status}'
            )
            
            return Response({'status': new_status})
        
        return Response(
            {'error': 'Неверный статус'},
            status=status.HTTP_400_BAD_REQUEST
        )


class FileDownloadView(generics.RetrieveAPIView):
    """View для скачивания файла"""
    
    permission_classes = [IsAuthenticated]
    queryset = GeneratedFile.objects.all()
    
    def retrieve(self, request, *args, **kwargs):
        file_obj = self.get_object()
        file_path = file_obj.file_path.path
        
        if os.path.exists(file_path):
            response = FileResponse(
                open(file_path, 'rb'),
                as_attachment=True,
                filename=file_obj.file_name
            )
            return response
        
        return Response(
            {'error': 'Файл не найден'},
            status=status.HTTP_404_NOT_FOUND
        )