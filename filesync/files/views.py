from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import SyncedFile
from .serializers import SyncedFileSerializer

# Create your views here.

# RESTful implementation of file operations
class SyncedFileViewSet(viewsets.ViewSet):

    # List all uploaded files.
    def list(self, request):
        files = SyncedFile.objects.all()
        serializer = SyncedFileSerializer(files, many=True)
        return Response(serializer.data)

    # Get info on a certain uploaded file
    def retrieve(self, request, pk=None):
        file = get_object_or_404(SyncedFile, pk=pk)
        serializer = SyncedFileSerializer(file)
        return Response(serializer.data)

    # Upload a new file
    def create(self, request):
        serializer = SyncedFileSerializer(data=request.data)
        if serializer.is_valid():
            #print("valid")
            obj = serializer.save()
            #print(f"saved {obj}")
            return Response(serializer.data, status=201)
        #print("error:", serializer.errors)
        return Response(serializer.errors, status=400)

    # Update an existing file
    def update(self, request, pk=None):
        file = get_object_or_404(SyncedFile, pk=pk)
        serializer = SyncedFileSerializer(file, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    # Delete a file
    def destroy(self, request, pk=None):
        file = get_object_or_404(SyncedFile, pk=pk)
        file.delete()
        return Response(status=204)