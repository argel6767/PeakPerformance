from rest_framework import permissions

'''
only allows requests by admin level users
'''
class isAdminUser(permissions.BasePermission):
    def has_permission(self, request):
        return bool(request.user and request.user.is_staff)