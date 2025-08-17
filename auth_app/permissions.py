from rest_framework.permissions import BasePermission

class IsPatient(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and 
            (request.user.role == 'PATIENT' or request.user.is_superuser)
        )


class IsDoctor(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and 
            (request.user.role == 'DOCTOR' or request.user.is_superuser)
        )


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_superuser
