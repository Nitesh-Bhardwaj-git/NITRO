from django.urls import path
from . import views


urlpatterns = [
    path('files', views.files_collection, name='files_collection_no_slash'),
    path('files/', views.files_collection, name='files_collection'),
    path('files/<uuid:file_id>', views.file_resource, name='file_resource_no_slash'),
    path('files/<uuid:file_id>/', views.file_resource, name='file_resource'),
    path('files/<uuid:file_id>/progress', views.get_progress, name='get_progress_no_slash'),
    path('files/<uuid:file_id>/progress/', views.get_progress, name='get_progress'),
]

