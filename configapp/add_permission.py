from rest_framework.permissions import BasePermission

class TeacherPermission(BasePermission):
    """
        Teacher: faqat GET va PATCH qilishga ruxsat
        Admin: to'liq CRUD
    """
    def has_permission(self, request, view):
        if request.user.is_admin:
            return True

        if request.user.is_teacher and request.method in ['GET', 'PATCH']:
            return True

        return False
