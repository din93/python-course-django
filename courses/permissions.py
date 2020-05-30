from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsTeacherOrStudentReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.is_user_teacher(request.user):
            return True
        elif obj.is_user_student(request.user) and request.method in SAFE_METHODS:
            return True
        elif request.user.is_superuser:
            return True
        else:
            return False

class IsStudentOrTeacherReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.is_user_student(request.user):
            return True
        elif obj.is_user_teacher(request.user) and request.method in SAFE_METHODS:
            return True
        elif request.user.is_superuser:
            return True
        else:
            return False
