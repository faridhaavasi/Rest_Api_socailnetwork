from rest_framework import permissions

class IsAuthorOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        return  obj.author == request.user
    