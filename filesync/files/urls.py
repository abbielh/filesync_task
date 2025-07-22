from django.urls import path
from .views import SyncedFileViewSet

file_list = SyncedFileViewSet.as_view({'get': 'list', 'post': 'create'})
file_detail = SyncedFileViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})

# files/ path used to list all files and create files on the server
# files/<int:pk>/ used to get, delete and update certain files existing on the server by their IDs
urlpatterns = [
    path('files/', file_list, name='file-list'),
    path('files/<int:pk>/', file_detail, name='file-detail'),
]
