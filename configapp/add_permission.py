from rest_framework.permissions import BasePermission

# Admin uchun to'liq CRUD
class AdminPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.is_admin:
            return True

        return False


# Admin va Staff uchun to'liq CRUD
class StaffPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.is_staff or request.user.is_admin:
            return True

        return False


# Teacher: faqat GET va POST qilishga ruxsat
# Admin va Staff: to'liq CRUD
class TeacherPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.is_admin or request.user.is_staff:
            return True

        if request.user.is_authenticated and request.user.is_teacher and request.method in ['GET', 'POST']:
            return True

        return False


# Teacher: faqat PATCH qilishga ruxsat
# Admin va Staff: to'liq CRUD
class TeacherUpdatePermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.is_admin or request.user.is_staff:
            return True

        if request.user.is_authenticated and request.user.is_teacher and request.method in ['PATCH']:
            return True

        return False


# Student: faqat GET va POST qilishga ruxsat
# Admin va Staff: to'liq CRUD
class StudentPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.is_admin or request.user.is_staff:
            return True

        if request.user.is_authenticated and request.user.is_student and request.method in ['GET', 'POST']:
            return True

        return False
