from django.db import models
from .auth_users import *

# Fanlar
class Course(BaseModel):
    title = models.CharField(max_length=50)
    descriptions = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.title

# Xodimlar darajasini belgilash
class Department(BaseModel):
    title = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    descriptions = models.CharField(max_length=500, null=True, blank=True)
    search_fields = ['user__phone', 'user__full_name']

    def __str__(self):
        return self.title

# Xodimlar datalarini saqlash
class Teacher(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ManyToManyField(Department, related_name='get_teacher')
    course = models.ManyToManyField(Course, related_name='get_course')
    descriptions = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.user.phone_number
