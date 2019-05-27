from rest_framework import permissions


class UserPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if -626 in request.user.groups:
            return True
        if request.user == obj:
            return True
        return False


class UserNPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        print(request.user.groups)
        if -626 in request.user.groups:
            return True
        return False
