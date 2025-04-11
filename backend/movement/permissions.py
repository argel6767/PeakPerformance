from rest_framework import permissions

'''
only allows requests by admin level users
'''
class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff)
    