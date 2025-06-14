from rest_framework import permissions


class IsTeacherPermission(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_permission(self, request, view):
        return bool(request.user and
                    request.user.is_authenticated and
                    getattr(request.user,'role',None)=="teacher")


