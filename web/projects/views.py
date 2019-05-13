from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import Project
from .serializers import ProjectSerializer


class ProjectAPIViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    lookup_field = 'pid'
    serializer_class = ProjectSerializer

    def list(self, request):
        # admin
        return super().list(request)

    def retrieve(self, request, pid=None):
        # if admin or user
        pass

    def create(self, request):
        # if admin
        return super().create(request)

    def update(self, request, pid=None):
        # if admin or user
        # if admin check name, group
        return super().update(request, pid=pid)

    def partial_update(self, request, pid=None):
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)

    def destroy(self, request, pid=None):
        # if super admin
        return super().destory(request, pid=pid)
