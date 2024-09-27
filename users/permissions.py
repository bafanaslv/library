from rest_framework.permissions import BasePermission


class IsLibrarian(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name="librarian").exists()
