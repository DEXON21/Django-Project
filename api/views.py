from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions
from .models import Client, Project
from .serializers import ClientSerializer, ProjectSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        client_id = self.kwargs.get('client_pk')
        client = Client.objects.get(pk=client_id)
        serializer.save(created_by=self.request.user, client=client)

    def get_queryset(self):
        if 'client_pk' in self.kwargs:
            return self.queryset.filter(client_id=self.kwargs['client_pk'])
        return self.queryset.filter(users=self.request.user)
