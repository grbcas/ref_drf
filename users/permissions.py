from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.pk == obj.pk


class IsProfileOwner(BasePermission):
    def has_permission(self, request, view):
        print(request.user.pk, view.kwargs.get('pk'))
        return request.user.pk == view.kwargs.get('pk')
