from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import User
from .serializers import UserSerializer


class UserAPIViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    lookup_field = 'uid'
    serializer_class = UserSerializer

    def list(self, request):
        # admin
        return super().list(request)

    def retrieve(self, request, uid=None):
        # if admin or user
        return super().retrieve(request, uid=uid)

    def create(self, request):
        # if admin
        return super().create(request)

    def update(self, request, uid=None):
        # if admin or user
        # if not admin check name, group
        return super().update(request, uid=uid)

    def partial_update(self, request, uid=None):
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)

    def destroy(self, request, pid=None):
        # if super admin
        return super().destory(request, pid=pid)
