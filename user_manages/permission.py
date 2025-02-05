from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    """
    Custom permission to allow only Admin users full access.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "admin"


class IsMemberUser(permissions.BasePermission):
    """
    Custom permission to allow only Member users to view books and borrow/return them.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "member"
