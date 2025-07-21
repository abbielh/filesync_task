from django.urls import path
from .views import SyncedFileViewSet

file_list = SyncedFileViewSet.as_view({'get': 'list', 'post': 'create'})
file_detail = SyncedFileViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})

urlpatterns = [
    path('files/', file_list, name='file-list'),
    path('files/<int:pk>/', file_detail, name='file-detail'),
]
